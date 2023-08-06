"""testing the default import"""
import os

from tempfile import TemporaryDirectory
from unittest import TestCase, main

from cogent3 import available_apps
from cogent3.app import align, dist, evo, io, sample, translate, tree
from cogent3.app.composable import (
    LOADER,
    WRITER,
    __app_registry,
    define_app,
    is_composable,
)
from cogent3.util.misc import get_object_provenance
from cogent3.util.table import Table


__author__ = "Gavin Huttley"
__copyright__ = "Copyright 2007-2022, The Cogent Project"
__credits__ = ["Gavin Huttley", "Nick Shahmaras"]
__license__ = "BSD-3"
__version__ = "2022.10.31a1"
__maintainer__ = "Gavin Huttley"
__email__ = "Gavin.Huttley@anu.edu.au"
__status__ = "Alpha"


def _get_all_composables(tmp_dir_name):
    test_model1 = evo.model("HKY85")
    test_model2 = evo.model("GN")
    test_hyp = evo.hypothesis(test_model1, test_model2)
    test_num_reps = 100

    return [
        align.align_to_ref(),
        align.progressive_align(model="GY94"),
        dist.fast_slow_dist(moltype="dna", fast_calc="hamming"),
        evo.ancestral_states(),
        evo.bootstrap(hyp=test_hyp, num_reps=test_num_reps),
        evo.hypothesis(test_model1, test_model2),
        evo.model("GN"),
        evo.tabulate_stats(),
        sample.fixed_length(100),
        sample.min_length(100),
        io.write_db(tmp_dir_name, create=True),
        io.write_json(tmp_dir_name, create=True),
        io.write_seqs(tmp_dir_name, create=True),
        sample.omit_bad_seqs(),
        sample.omit_degenerates(),
        sample.omit_duplicated(),
        sample.take_codon_positions(1),
        sample.take_named_seqs(),
        sample.take_n_seqs(2),
        sample.trim_stop_codons(gc=1),
        translate.select_translatable(),
        tree.quick_tree(),
        tree.scale_branches(),
        tree.uniformize_tree(),
    ]


class TestAvailableApps(TestCase):
    def test_available_apps(self):
        """available_apps returns a table"""
        from cogent3.util.table import Table

        apps = available_apps()
        self.assertIsInstance(apps, Table)
        self.assertTrue(apps.shape[0] > 10)

    def test_composable_pairwise_applications(self):
        """Properly compose two composable applications"""

        with TemporaryDirectory(dir=".") as dirname:
            applications = _get_all_composables(os.path.join(dirname, "delme"))
            for app in applications:
                self.assertTrue(is_composable(app), msg=app)

            composable_application_tuples = [
                (app1, app2)
                for app1 in applications
                for app2 in applications
                if app1 != app2
                and (
                    app1._return_types & app2._data_types
                    or app1._return_types & {"SerialisableType", "IdentifierType"}
                )
                and app1.app_type is not WRITER
                and app2.app_type is not LOADER
            ]

            for app_a, app_b in composable_application_tuples:
                app_a.disconnect()
                app_b.disconnect()
                # Compose two composable applications, there should not be exceptions.
                app_a + app_b

            for app in applications:
                if hasattr(app, "data_store"):
                    app.data_store.close()

    def test_incompatible_pairwise_applications(self):
        """Properly identify two incompatible applications"""

        with TemporaryDirectory(dir=".") as dirname:
            applications = _get_all_composables(os.path.join(dirname, "delme"))
            for app in applications:
                self.assertTrue(is_composable(app))

            incompatible_application_tuples = [
                (app1, app2)
                for app1 in applications
                for app2 in applications
                if app1.app_type is WRITER
                or app2.app_type is LOADER
                and app1 != app2
                and not app1._return_types & app2._data_types
                and not app1._return_types & {"SerialisableType", "IdentifierType"}
            ]

            for app_a, app_b in incompatible_application_tuples:
                err_type = ValueError if app_a is app_b else TypeError
                app_a.disconnect()
                app_b.disconnect()

                # Compose two incompatible applications, there should be exceptions.
                with self.assertRaises(err_type):
                    app_a + app_b

            for app in applications:
                if hasattr(app, "data_store"):
                    app.data_store.close()


def test_available_apps_local():
    """available_apps robust to local scope apps"""

    @define_app
    def dummy(val: int) -> int:
        return val

    apps = available_apps()
    assert isinstance(apps, Table)
    __app_registry.pop(get_object_provenance(dummy), None)


if __name__ == "__main__":
    main()
