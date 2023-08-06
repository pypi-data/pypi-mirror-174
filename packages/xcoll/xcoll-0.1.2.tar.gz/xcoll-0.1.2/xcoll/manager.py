import numpy as np
import pandas as pd

from .beam_elements import BlackAbsorber, K2Collimator, K2Crystal, _all_collimator_types
from .scattering_routines.k2 import K2Engine
from .colldb import CollDB
from .tables import CollimatorImpacts

import xtrack as xt
import xobjects as xo



class CollimatorManager:
    def __init__(self, *, line, line_is_reversed=False, colldb: CollDB, capacity=1e6, record_impacts=False, \
                 _context=None, _buffer=None, io_buffer=None):

        if not isinstance(colldb, CollDB):
            raise ValueError("The variable 'colldb' needs to be an xcoll CollDB object!")
        else:
            self.colldb = colldb
        if not isinstance(line, xt.Line):
            raise ValueError("The variable 'line' needs to be an xtrack Line object!")
        else:
            self.line = line
        self._k2engine = None   # only needed for FORTRAN K2Collimator

        # Create _buffer, _context, and _io_buffer
        if _buffer is None:
            if _context is None:
                _context = xo.ContextCpu()
            _buffer = _context.new_buffer()
        elif _context is not None and _buffer.context != _context:
            raise ValueError("The provided buffer and context do not match! "
                             + "Make sure the buffer is generated inside the provided context, or alternatively, "
                             + "only pass one of _buffer or _context.")
        self._buffer = _buffer
        # TODO: currently capacity is only for io_buffer (hence for _impacts). Do we need it in the _buffer as well?
        self._capacity = int(capacity)
        if io_buffer is None:
            io_buffer = xt.new_io_buffer(_context=self._buffer.context, capacity=self.capacity)
        elif self._buffer.context != io_buffer._context:
            raise ValueError("The provided io_buffer lives on a different context than the buffer!")
        self._io_buffer = io_buffer

        # Initialise impacts table
        self._record_impacts = []
        self._impacts = None
        self.record_impacts = record_impacts

        self.tracker = None
        self._losmap = None
        self._coll_summary = None
        self._line_is_reversed = line_is_reversed


    @property
    def impacts(self):
        interactions = {
            -1: 'Black', 1: 'Nuclear-Inelastic', 2: 'Nuclear-Elastic', 3: 'pp-Elastic', 4: 'Single-Diffractive', 5: 'Coulomb'
        }
        n_rows = self._impacts._index + 1
        df = pd.DataFrame({
                'collimator':        [self.line.element_names[elemid] for elemid in self._impacts.at_element[:n_rows]],
                's':                 self._impacts.s[:n_rows],
                'turn':              self._impacts.at_turn[:n_rows],
                'interaction_type':  [ interactions[int_id] for int_id in self._impacts.interaction_type[:n_rows] ],
            })
        cols = ['id', 'x', 'px', 'y', 'py', 'zeta', 'delta', 'energy', 'mass', 'charge', 'z', 'a', 'pdgid']
        for particle in ['parent', 'child']:
            multicols = pd.MultiIndex.from_tuples([(particle, col) for col in cols])
            newdf = pd.DataFrame(index=df.index, columns=multicols)
            for col in cols:
                newdf[particle, col] = getattr(self._impacts,particle + '_' + col)[:n_rows]
            df = pd.concat([df, newdf], axis=1)
        return df

    @property
    def record_impacts(self):
        return self._record_impacts

    @record_impacts.setter
    def record_impacts(self, record_impacts):
        # TODO: how to get impacts if different collimator types in line?
        if record_impacts is True:
            record_impacts = self.collimator_names
        elif record_impacts is False or record_impacts is None:
            record_impacts = []
        record_start = set(record_impacts) - set(self._record_impacts)
        record_stop = set(self._record_impacts) - set(record_impacts)
        if record_start:
            if self._impacts is None:
                self._impacts = xt.start_internal_logging(io_buffer=self._io_buffer, capacity=self.capacity, \
                                                          elements=record_start)
            else:
                xt.start_internal_logging(io_buffer=self._io_buffer, capacity=self.capacity, \
                                          record=self._impacts, elements=record_start)
        if record_stop:
            if self.tracker is not None:
                self.tracker._check_invalidated()
            xt.stop_internal_logging(elements=record_stop)
        self._record_impacts = record_impacts

    @property
    def capacity(self):
        return self._capacity

    @capacity.setter
    def capacity(self, capacity):
        capacity = int(capacity)
        if capacity < self.capacity:
            raise NotImplementedError("Shrinking of capacity not yet implemented!")
        elif capacity == self.capacity:
            return
        else:
            self._io_buffer.grow(capacity-self.capacity)
            if self._impacts is not None:
                # TODO: increase capacity of iobuffer AND of _impacts
                raise NotImplementedError

    @property
    def collimator_names(self):
        return list(self.colldb.name)

    @property
    def s_start(self):
        return self.colldb.s_center - self.colldb.active_length/2 - self.colldb.inactive_front

    @property
    def s_start_active(self):
        return self.colldb.s_center - self.colldb.active_length/2

    @property
    def s_center(self):
        return self.colldb.s_center

    @property
    def s_end_active(self):
        return self.colldb.s_center + self.colldb.active_length/2

    @property
    def s_end(self):
        return self.colldb.s_center + self.colldb.active_length/2 + self.colldb.inactive_back

    @property
    def s_match(self):
        return self.colldb.s_match

    def install_black_absorbers(self, names=None, *, verbose=False):
        def install_func(thiscoll, name):
            return BlackAbsorber(
                    inactive_front=thiscoll['inactive_front'],
                    inactive_back=thiscoll['inactive_back'],
                    active_length=thiscoll['active_length'],
                    angle=thiscoll['angle'],
                    is_active=False
                   )
        self._install_collimators(names, collimator_class=BlackAbsorber, install_func=install_func, verbose=verbose)


    def install_k2_collimators(self, names=None, *, max_part=50000, seed=None, verbose=False):
        # Check for the existence of a K2Engine; warn if settings are different
        # (only one instance of K2Engine should exist).
        if seed is None:
            seed = np.random.randint(1, 10000000)
        if self._k2engine is None:
            self._k2engine = K2Engine(n_alloc=max_part, random_generator_seed=seed)
        else:
            if self._k2engine.n_alloc != max_part:
                print(f"Warning: K2 already initiated with a maximum allocation of {self._k2engine.n_alloc} particles.\n"
                      + f"Ignoring the requested max_part={max_part}.")
            if self._k2engine.random_generator_seed != seed:
                print(f"Warning: K2 already initiated with seed {self._k2engine.random_generator_seed}.\n"
                      + f"Ignoring the requested seed={seed}.")

        # Do the installation
        def install_func(thiscoll, name):
            return K2Collimator(
                    k2engine=self._k2engine,
                    inactive_front=thiscoll['inactive_front'],
                    inactive_back=thiscoll['inactive_back'],
                    active_length=thiscoll['active_length'],
                    angle=thiscoll['angle'],
                    material=thiscoll['material'],
                    is_active=False
                   )
        self._install_collimators(names, collimator_class=K2Collimator, install_func=install_func, verbose=verbose)


    def _install_collimators(self, names, *, collimator_class, install_func, verbose):
        # Check that collimator marker exists in Line and CollDB,
        # and that tracker is not yet built
        line = self.line
        df = self.colldb._colldb
        if names is None:
            names = self.collimator_names
        mask = df.index.isin(names)
        for name in names:
            if name not in line.element_names:
                raise Exception(f"Collimator {name} not found in line!")
            elif name not in self.collimator_names:
                print(f"Warning: Collimator {name} not found in CollDB! Ignoring...")
        if line.tracker is not None:
            raise Exception("Tracker already built!\nPlease install collimators before building tracker!")

        # Get collimator centers
        positions = dict(zip(names,line.get_s_position(names)))

        # Loop over collimators to install
        for name in names:

            # Check that collimator is not installed as different type
            # TODO: automatically replace collimator type and print warning
            for other_coll_class in _all_collimator_types - {collimator_class}:
                if isinstance(line[name], other_coll_class):
                    raise ValueError(f"Trying to install {name} as {collimator_class.__name__},"
                                     + f" but it is already installed as {other_coll_class.__name__}!\n"
                                     + "Please reconstruct the line.")

            # Check that collimator is not installed previously
            if isinstance(line[name], collimator_class):
                if df.loc[name,'collimator_type'] != collimator_class.__name__:
                    raise Exception(f"Something is wrong: Collimator {name} already installed in line "
                                    + f"as {collimator_class.__name__} element, but registered in CollDB "
                                    + f"as {df.loc[name,'collimator_type']}. Please reconstruct the line.")
                if verbose:
                    print(f"Collimator {name} already installed. Skipping...")
            else:
                if verbose:
                    print(f"Installing {name}")
                # Get the settings from the CollDB
                thiscoll = df.loc[name]
                # Create the collimator element
                newcoll = install_func(thiscoll, name)
                # Update the position and type in the CollDB
                df.loc[name,'s_center'] = positions[name]
                df.loc[name,'collimator_type'] = collimator_class.__name__
                # Do the installation
                s_install = df.loc[name,'s_center'] - thiscoll['active_length']/2 - thiscoll['inactive_front']
                if name+'_aper' in line.element_names:
                    coll_aper = line[name+'_aper']
                    assert coll_aper.__class__.__name__.startswith('Limit')
                    if np.any([name+'_aper_tilt_' in nn for nn in line.element_names]):
                        raise NotImplementedError("Collimator apertures with tilt not implemented!")
                    if np.any([name+'_aper_offset_' in nn for nn in line.element_names]):
                        raise NotImplementedError("Collimator apertures with offset not implemented!")
                else:
                    coll_aper = None

                line.insert_element(element=newcoll, name=name, at_s=s_install)

                if coll_aper is not None:
                    line.insert_element(element=coll_aper, name=name+'_aper_front', index=name)
                    line.insert_element(element=coll_aper, name=name+'_aper_back',
                                        index=line.element_names.index(name)+1)



    def align_collimators_to(self, align):
        if any([ x is None for x in self.colldb.collimator_type ]):
            raise ValueError("Some collimators have not yet been installed.\n"
                             + "Please install all collimators before aligning the collimators.")
        self.colldb.align_to = align


    def build_tracker(self, **kwargs):
        kwargs.setdefault('_buffer', self._buffer)
        kwargs.setdefault('io_buffer', self._io_buffer)
        if kwargs['_buffer'] != self._buffer:
            raise ValueError("Cannot build tracker with different buffer than the CollimationManager buffer!")
        if kwargs['io_buffer'] != self._io_buffer:
            raise ValueError("Cannot build tracker with different io_buffer than the CollimationManager io_buffer!")
        if '_context' in kwargs and kwargs['_context'] != self._buffer.context:
            raise ValueError("Cannot build tracker with different context than the CollimationManager context!")
        self.tracker = self.line.build_tracker(**kwargs)
        return self.tracker


    def _compute_optics(self, recompute=False):
        line = self.line
        if line is None or line.tracker is None:
            raise Exception("Please build tracker before computing the optics for the openings!")
        if np.any(
            [x is None for x in self.colldb._colldb.s_align_front]
            + [ x is None for x in self.colldb._colldb.s_align_back]
        ):
            raise Exception("Not all collimators are aligned! Please call 'align_collimators_to' "
                            + "on the CollimationManager before computing the optics for the openings!")

        pos = list(self.colldb._optics_positions_to_calculate)
        if recompute or pos != {}:
            tracker = self.line.tracker
            # Calculate optics without collimators
            old_val = {}
            for name in self.collimator_names:
                old_val[name] = line[name].is_active
                line[name].is_active = False
            tw = tracker.twiss(at_s=pos)
            self.colldb._optics = pd.concat([
                                    self.colldb._optics,
                                    pd.DataFrame({
                                        opt: tw[opt] for opt in self.colldb._optics.columns
                                    },index=pos)
                                ])
            for name in self.collimator_names:
                line[name].is_active = old_val[name]
            self.colldb._optics_positions_to_calculate = {}
            self.colldb.gamma_rel = tracker.particle_ref._xobject.gamma0[0]


    # The variable 'gaps' is meant to specify temporary settings that will overrule the CollDB.
    # As such, its settings will be applied to the collimator elements in the line, but not
    # written to the CollDB. Hence two successive calls to set_openings will not be combined,
    # and only the last call will be applied to the line.
    # The variable 'to_parking' will send all collimators that are not listed in 'gaps' to parking.
    # Similarily, the variable 'full_open' will set all openings of the collimators that are not
    # listed in 'gaps' to 1m.
    def set_openings(self, gaps={}, *, recompute_optics=False, to_parking=False, full_open=False):
        line = self.line
        if line is None or line.tracker is None:
            raise Exception("Please build tracker before calling this method!")
        colldb = self.colldb
        if any([ x is None for x in colldb.collimator_type ]):
            raise ValueError("Some collimators have not yet been installed.\n"
                             + "Please install all collimators before setting the openings.")
        if to_parking and full_open:
            raise ValueError("Cannot send collimators to parking and open them fully at the same time!")

        gaps_OLD = colldb.gap
        names = self.collimator_names
        # Override gap if sending to parking
        if to_parking:
            gaps = { **{ name: None for name in names }, **gaps }
        colldb.gap = gaps

        # Get the optics (to compute the opening)
        self._compute_optics(recompute=recompute_optics)
        if not self.colldb._optics_is_ready:
            raise Exception("Something is wrong: not all optics needed for the jaw openings are calculated!")

        # Configure collimators
        for name in names:
            # Override openings if opening fully
            if full_open and name not in gaps.keys():
                line[name].is_active = False
            # Apply settings to element
            elif isinstance(line[name], BlackAbsorber):
                line[name].dx = colldb.x[name]
                line[name].dy = colldb.y[name]
                line[name].angle = colldb.angle[name]
                line[name].jaw_F_L = colldb._colldb.jaw_F_L[name]
                line[name].jaw_F_R = colldb._colldb.jaw_F_R[name]
                line[name].jaw_B_L = colldb._colldb.jaw_B_L[name]
                line[name].jaw_B_R = colldb._colldb.jaw_B_R[name]
                line[name].is_active = colldb.is_active[name]
            elif isinstance(line[name], K2Collimator):
                line[name].material = colldb.material[name]
                line[name].dx = colldb.x[name]
                line[name].dy = colldb.y[name]
                line[name].dpx = colldb.px[name]   # This is a K2 curiosity; we don't want it in our future code
                line[name].dpy = colldb.py[name]   # This is a K2 curiosity; we don't want it in our future code
                line[name].angle = colldb.angle[name]
                line[name].jaw_F_L = colldb._colldb.jaw_F_L[name]
                line[name].jaw_F_R = colldb._colldb.jaw_F_R[name]
                line[name].jaw_B_L = colldb._colldb.jaw_B_L[name]
                line[name].jaw_B_R = colldb._colldb.jaw_B_R[name]
                if colldb.onesided[name] == 'both':
                    line[name].onesided = False
                elif colldb.onesided[name] == 'left':
                    line[name].onesided = True
                elif colldb.onesided[name] == 'right':
                    raise ValueError(f"Right-sided collimators not implemented for K2Collimator {name}!")
                line[name].is_active = colldb.is_active[name]
            else:
                raise ValueError(f"Missing implementation for element type of collimator {name}!")
        colldb.gap = gaps_OLD


    def track(self, *args, **kwargs):
        self.tracker.track(*args, **kwargs)


    @property
    def lossmap(self):
        return self._lossmap

    def coll_summary(self, part):

        coll_s, coll_names, coll_length = self._get_collimator_losses(part)

        names = dict(zip(coll_s, coll_names))
        lengths = dict(zip(coll_s, coll_length))
        s = sorted(list(names.keys()))
        collname    =  [ names[pos] for pos in s ]
        colllengths =  [ lengths[pos] for pos in s ]
        nabs = []
        for pos in s:
            nabs.append(coll_s.count(pos))

        return pd.DataFrame({
            "collname": collname,
            "nabs":     nabs,
            "length":   colllengths,
            "s":        s
        })


    def create_lossmap(self, part, interpolation=0.1):
        # Loss location refinement
        if interpolation is not None:
            print("Performing the aperture losses refinement.")
            loss_loc_refinement = xt.LossLocationRefinement(self.tracker,
                    n_theta = 360, # Angular resolution in the polygonal approximation of the aperture
                    r_max = 0.5, # Maximum transverse aperture in m
                    dr = 50e-6, # Transverse loss refinement accuracy [m]
                    ds = interpolation, # Longitudinal loss refinement accuracy [m]
                    # save_refine_trackers=True # Diagnostics flag
                    )
            loss_loc_refinement.refine_loss_location(part)

        coll_s, coll_names, coll_length = self._get_collimator_losses(part)
        aper_s, aper_names              = self._get_aperture_losses(part)

        self._lossmap = {
            'collimator': {
                's':      coll_s,
                'name':   coll_names,
                'length': coll_length
            }
            ,
            'aperture': {
                's':    aper_s,
                'name': aper_names
            }
            ,
            'machine_length': self.line.get_length()
            ,
            'interpolation': interpolation
            ,
            'reversed': self._line_is_reversed
        }

        return self.lossmap

    def _get_collimator_losses(self, part):
        coll_names = [self.line.element_names[i] for i in part.at_element[part.state==-333]]
        # TODO: this way to get the collimator positions is a hack that needs to be cleaner with the new API
        coll_positions = dict(zip(self.collimator_names, self.s_center))
        coll_s = [coll_positions[name] for name in coll_names]
        coll_length = [self.line[i].active_length for i in part.at_element[part.state==-333]]
        machine_length = self.line.get_length()
        if self._line_is_reversed:
            coll_s = [ machine_length - s for s in coll_s ]

        return coll_s, coll_names, coll_length


    def _get_aperture_losses(self, part):

        aper_s = list(part.s[part.state==0])
        aper_names = [self.line.element_names[i] for i in part.at_element[part.state==0]]
        machine_length = self.line.get_length()
        if self._line_is_reversed:
            aper_s = [ machine_length - s for s in aper_s ]

        return aper_s, aper_names

