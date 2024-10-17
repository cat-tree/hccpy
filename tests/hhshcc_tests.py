import unittest
import numpy as np
from hccpy.hhshcc import HHSHCCEngine


class TestHHSHCCEngine(unittest.TestCase):

    def assert_items_in_rp(self, rp, expected_hccs):
        for hcc in expected_hccs:
            with self.subTest(f"Checking {hcc} in rp"):
                self.assertTrue(hcc in rp["details"],
                                f"{hcc} not found")

    def test_hccmapping_y19(self):
        hhe = HHSHCCEngine(myear="2019")
        rp = hhe.profile(["E1169"])
        self.assertTrue("G01" in rp["details"])
        self.assertTrue("HHS_HCC020" in rp["hcc_map"].values())

        rp = hhe.profile(["P0411"], age=1)
        self.assertTrue("AGE1_X_SEVERITY2" in rp["details"])

        rp = hhe.profile(["P0411"], age=10)
        self.assertTrue(len(rp["hcc_lst"]) == 0)

        rp = hhe.profile(["E1169", "I5030", "I509", "I211", "I209", "R05"])
        self.assertTrue("HHS_HCC130" in rp["details"])

        rp = hhe.profile([], rx_lst=["00003196401"], age=45)
        self.assertTrue("RXC_01" in rp["details"])

    def test_hccmapping_y22(self):
        hhe = HHSHCCEngine(myear="2022")
        rp = hhe.profile(["E1169"])
        self.assertTrue("G01" in rp["details"])
        self.assertTrue("HHS_HCC020" in rp["hcc_map"].values())

        rp = hhe.profile(["P0411"], age=1)
        self.assertTrue("AGE1_X_SEVERITY2" in rp["details"])

        rp = hhe.profile(["P0411"], age=10)
        self.assertTrue(len(rp["hcc_lst"]) == 0)

        rp = hhe.profile(["E1169", "I5030", "I509", "I211", "I209", "R05"])
        self.assertTrue("HHS_HCC130" in rp["details"])

        rp = hhe.profile([], rx_lst=["00003196401"], age=45)
        self.assertTrue("RXC_01" in rp["details"])

    def test_hccmapping_rx(self):
        hhe = HHSHCCEngine(myear="2022")
        rp = hhe.profile(["E1169"], pr_lst=["J1817"], age=30)
        self.assertTrue("RXC_06" in rp["details"])

    def test_hierarchy(self):
        hhe = HHSHCCEngine()  # defaults to 2022
        rp = hhe.profile(['O34219', 'Z3A29'], age=30)
        self.assertTrue("HHS_HCC212" not in rp["details"])

    def test_24_adult(self):
        hhe = HHSHCCEngine(myear="2024")
        rp = hhe.profile(['B20', 'J17469'],["J1746"], age=21)
        expected_hccs = ['RXC_01', 'HHS_HCC001', 'RXC_01_x_HCC001']
        self.assert_items_in_rp(rp, expected_hccs)

        rp = hhe.profile(["R6520", "A849", "S062X3A"], age=21)
        expected_hccs = ['HHS_HCC002', 'HHS_HCC003', 'HHS_HCC223', 'SEVERE_HCC_COUNT3']
        self.assert_items_in_rp(rp, expected_hccs)

        rp = hhe.profile(["Z944", "K750", "K717", "B182"], age=21)
        expected_hccs = ['HHS_HCC034', 'SEVERE_HCC_COUNT1']
        self.assert_items_in_rp(rp, expected_hccs)

        rp = hhe.profile(["E1110", "E0821", "E08649"], age=21)
        expected_hccs = ['G01']
        self.assert_items_in_rp(rp, expected_hccs)

        rp = hhe.profile(["M05721", "Z9482", "A021", "A203", "G031"],["J3380"], age=21)
        expected_hccs = ['RXC_09', 'HHS_HCC056', 'HHS_HCC041', 'HHS_HCC002', 'HHS_HCC003',
                                             'RXC_09_x_HCC056_057_and_048_041', 'RXC_09_x_HCC056',
                                             'RXC_09_x_HCC048_041', 'SEVERE_HCC_COUNT4', 'TRANSPLANT_HCC_COUNT4']
        self.assert_items_in_rp(rp, expected_hccs)

        rp = hhe.profile(["T794XXA", "A203", "G031", "B484", "C7800", "C220", "C8410", "C039", "C7650", "C430", "Z9483"], age=21)
        expected_hccs = ['HHS_HCC002', 'HHS_HCC006', 'HHS_HCC008', 'G24', 'SEVERE_HCC_COUNT4']
        self.assert_items_in_rp(rp, expected_hccs)

        rp = hhe.profile(["Z9483", "Z944", "K750", "K743", "B182", "Z9482", "K261", "Q431", "K860"], age=21)
        expected_hccs = ['HHS_HCC034', 'HHS_HCC041', 'HHS_HCC042', 'HHS_HCC046', 'G24',
                                 'TRANSPLANT_HCC_COUNT4']
        self.assert_items_in_rp(rp, expected_hccs)

        rp = hhe.profile(["E0800", "E0821", "E08649", "E7603", "E7402", "Q780", "Q772"], age=21)
        expected_hccs = ['G01', 'G02B', 'G04']
        self.assert_items_in_rp(rp, expected_hccs)

    def test_24_child(self):
        hhe = HHSHCCEngine(myear="2024")
        rp = hhe.profile(["E1110", "E0821", "E08649"], age=4)
        expected_hccs = ['G01']
        self.assert_items_in_rp(rp, expected_hccs)

        rp = hhe.profile(["T794XXA", "M726"], age=11)
        expected_hccs = ['HHS_HCC002', 'G03', 'SEVERE_HCC_COUNT1']
        self.assert_items_in_rp(rp, expected_hccs)

        rp = hhe.profile(["Z9483", "E441", "E230", "Z944"], age=16)
        expected_hccs = ['HHS_HCC018', 'HHS_HCC023', 'HHS_HCC030', 'HHS_HCC034',
                                     'SEVERE_HCC_COUNT4', 'TRANSPLANT_HCC_COUNT4PLUS']
        self.assert_items_in_rp(rp, expected_hccs)

        rp = hhe.profile(["E7403", "E74810", "D571", "D562"], age=6)
        expected_hccs = ['G02B', 'G02D', 'G07A']
        self.assert_items_in_rp(rp, expected_hccs)

        rp = hhe.profile(["R6521", "G002", "B442", "C7800", "E41", "K8511","I301","S32309A"], age=19)
        expected_hccs = ['HHS_HCC002', 'HHS_HCC003', 'HHS_HCC006','HHS_HCC008','HHS_HCC023',
                                     'HHS_HCC047','HHS_HCC135','HHS_HCC226','SEVERE_HCC_COUNT8PLUS']
        self.assert_items_in_rp(rp, expected_hccs)

        rp = hhe.profile(["Z9483","E43","E15","Z944","Z9482","K651"], age=10)
        expected_hccs = ['HHS_HCC018', 'HHS_HCC023', 'HHS_HCC030','HHS_HCC034','HHS_HCC041', 'HHS_HCC042',
                         'SEVERE_HCC_COUNT6_7', 'TRANSPLANT_HCC_COUNT4PLUS']
        self.assert_items_in_rp(rp, expected_hccs)

    def test_24_infant(self):
        hhe = HHSHCCEngine(myear="2024")
        rp = hhe.profile(["C7800", "P0701"], age=0)
        expected_hccs = ['EXTREMELY_IMMATURE_X_SEVERITY5']
        self.assert_items_in_rp(rp, expected_hccs)

        # rp = hhe.profile(["A227", "B59", "C7B00"], age=0)
        # expected_hccs = ['TERM_X_SEVERITY5']
        # self.assert_items_in_rp(rp, expected_hccs)

        rp = hhe.profile(["E7402", "B182"], age=1)
        expected_hccs = ['AGE1_X_SEVERITY3']
        self.assert_items_in_rp(rp, expected_hccs)

        rp = hhe.profile(["B59", "C7B00","E7402","K750"], age=0)
        expected_hccs = ['TERM_X_SEVERITY5']
        self.assert_items_in_rp(rp, expected_hccs)

        rp = hhe.profile(["C7B00", "Z9483", "E1300", "E0821"], age=0)
        expected_hccs = ['TERM_X_SEVERITY5']
        self.assert_items_in_rp(rp, expected_hccs)

        rp = hhe.profile(["A227", "B59", "C7B00"], age=0)
        expected_hccs = ['TERM_X_SEVERITY5']
        self.assert_items_in_rp(rp, expected_hccs)

        rp = hhe.profile(["P0501", "Z387", "P081"], age=0)
        expected_hccs = ['EXTREMELY_IMMATURE_X_SEVERITY1']
        self.assert_items_in_rp(rp, expected_hccs)

        rp = hhe.profile([], age=0)
        expected_hccs = ['TERM_X_SEVERITY1']
        self.assert_items_in_rp(rp, expected_hccs)



if __name__ == "__main__":
    unittest.main()

