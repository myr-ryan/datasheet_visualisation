import unittest
from Plot_Data import *

class TestData(unittest.TestCase):

    
    def test_data_type(self):

        empty_data = {'x':[],'y':[]}
        plot_data = Plot_Data(empty_data)

        # The link for excel should be customized
        f = '/Users/ryanma/Library/CloudStorage/OneDrive-King\'sCollegeLondon/kings/Datasheet.xlsx'
        df_temp = pd.read_excel(f, sheet_name='Sheet1', engine='openpyxl')
        plot_data.upload_data(df_temp)
        plot_data.preprocessing()

        df = pd.DataFrame(plot_data.source.data)
        self.assertEqual(df['task'].dtypes, 'category')
        self.assertEqual(df['subspec'].dtypes, 'category')
        self.assertEqual(df['subspec'].dtypes, 'category')
        self.assertEqual(df['Paper ID'].dtypes, 'float')
        self.assertEqual(df['Title'].dtypes, 'string')
        self.assertEqual(df['ml_task_description'].dtypes, 'category')
        self.assertEqual(df['patient_num'].dtypes, 'float')
        self.assertEqual(df['image_type'].dtypes, 'category')
        self.assertEqual(df['data_size_all'].dtypes, 'float')
        self.assertEqual(df['data_size_validation'].dtypes, 'float')
        self.assertEqual(df['data_size_testing'].dtypes, 'float')
        self.assertEqual(df['data_size_training'].dtypes, 'float')
        # TODO
        self.assertEqual(df['explainability'].dtypes, 'string')
        self.assertEqual(df['balanced'].dtypes, 'bool')
        self.assertEqual(df['balanced_comment'].dtypes, 'string')
        self.assertEqual(df['bias'].dtypes, 'string')
        self.assertEqual(df['class_labels'].dtypes, 'string')
        self.assertEqual(df['data_source'].dtypes, 'string')
        self.assertEqual(df['data_links'].dtypes, 'string')
        self.assertEqual(df['raw data availability'].dtypes, 'category')
        self.assertEqual(df['processed data availability'].dtypes, 'category')
        self.assertEqual(df['code availability'].dtypes, 'bool')
        self.assertEqual(df['code_links'].dtypes, 'string')
        self.assertEqual(df['gender'].dtypes, 'category')
        self.assertEqual(df['age specified'].dtypes, 'string')

        # self.assertEqual(df['task_seg+obj_det'].dtypes, 'bool')
        # self.assertEqual(df['task_detection'].dtypes, 'bool')
        # self.assertEqual(df['task_diagnosis'].dtypes, 'bool')
        # self.assertEqual(df['task_prognosis'].dtypes, 'bool')
        # self.assertEqual(df['task_treatment_design'].dtypes, 'bool')
        self.assertEqual(df['treatment design comment'].dtypes, 'string')
        # self.assertEqual(df['task_risk prediction'].dtypes, 'bool')
        self.assertEqual(df['risk prediction comment'].dtypes, 'string')
        # self.assertEqual(df['task_subtyping'].dtypes, 'bool')
        # self.assertEqual(df['task_others'].dtypes, 'bool')
        self.assertEqual(df['task_others (specify)'].dtypes, 'string')     
        # self.assertEqual(df['subspec_ovarian'].dtypes, 'bool')
        # self.assertEqual(df['subspec_cervical'].dtypes, 'bool')
        # self.assertEqual(df['subspec_endometrial'].dtypes, 'bool')
        # self.assertEqual(df['subspec_metastasis'].dtypes, 'bool')
        # self.assertEqual(df['subspec_others'].dtypes, 'bool')
        self.assertEqual(df['subspec_others (specify)'].dtypes, 'string')
        self.assertEqual(df['performance_auc'].dtypes, 'float')
        self.assertEqual(df['performance_precision (PPV)'].dtypes, 'float')
        self.assertEqual(df['performance_specificity'].dtypes, 'float')
        self.assertEqual(df['performance_NPV'].dtypes, 'float')
        self.assertEqual(df['performance_sensitivity (recall)'].dtypes, 'float')
        self.assertEqual(df['performance_F1'].dtypes, 'float')
        self.assertEqual(df['performance_accuracy'].dtypes, 'float')
        self.assertEqual(df['performance_mean'].dtypes, 'float')
        self.assertEqual(df['neural network type'].dtypes, 'category')
        self.assertEqual(df['data collection technology'].dtypes, 'category')
        self.assertEqual(df['algorithm-pipeline'].dtypes, 'string')
        self.assertEqual(df['comments'].dtypes, 'string')
        self.assertEqual(df['year'].dtypes, 'float')
        self.assertEqual(df['ID'].dtypes, 'float')
        self.assertEqual(df['pmid'].dtypes, 'float')
        self.assertEqual(df['doi'].dtypes, 'string')
        self.assertEqual(df['abstract'].dtypes, 'string')
        self.assertEqual(df['article_date'].dtypes, 'datetime64[ns]')
        self.assertEqual(df['pubmed_date'].dtypes, 'datetime64[ns]')
        self.assertEqual(df['journal'].dtypes, 'string')
        self.assertEqual(df['journal_short'].dtypes, 'string')
        self.assertEqual(df['journal_country'].dtypes, 'string')
        self.assertEqual(df['authors'].dtypes, 'category')
        self.assertEqual(df['author_affils'].dtypes, 'category')
        self.assertEqual(df['keywords'].dtypes, 'category')
        self.assertEqual(df['mesh_terms'].dtypes, 'string')
        self.assertEqual(df['references_pmids'].dtypes, 'string')
        self.assertEqual(df['feature'].dtypes, 'string')
        self.assertEqual(df['include'].dtypes, 'bool')
        self.assertEqual(df['mature'].dtypes, 'bool')
        self.assertEqual(df['feat_xr'].dtypes, 'bool')
        self.assertEqual(df['feat_ct'].dtypes, 'bool')
        self.assertEqual(df['feat_mri'].dtypes, 'bool')
        self.assertEqual(df['feat_ecg'].dtypes, 'bool')
        self.assertEqual(df['feat_us'].dtypes, 'bool')
        self.assertEqual(df['feat_oct'].dtypes, 'bool')
        self.assertEqual(df['feat_mamm'].dtypes, 'bool')
        self.assertEqual(df['feat_endoscop'].dtypes, 'bool')
        self.assertEqual(df['feat_gene'].dtypes, 'bool')
        self.assertEqual(df['feat_bio'].dtypes, 'bool')
        self.assertEqual(df['feat_nlp'].dtypes, 'bool')
        self.assertEqual(df['feat_ehr'].dtypes, 'bool')
        # self.assertEqual(df['subspec_dermca'].dtypes, 'bool')
        # self.assertEqual(df['subspec_lungca'].dtypes, 'bool')
        # self.assertEqual(df['subspec_brainca'].dtypes, 'bool')
        # self.assertEqual(df['subspec_gica'].dtypes, 'bool')
        # self.assertEqual(df['subspec_hepca'].dtypes, 'bool')
        # self.assertEqual(df['subspec_prosca'].dtypes, 'bool')
        self.assertEqual(df['spec_gynonc'].dtypes, 'bool')
        # self.assertEqual(df['subspec_haemonc'].dtypes, 'bool')
        # self.assertEqual(df['subspec_breastca'].dtypes, 'bool')
        self.assertEqual(df['affil_countries'].dtypes, 'category')
        self.assertEqual(df['affil_countries_unique'].dtypes, 'category')
        self.assertEqual(df['affil_first_country'].dtypes, 'string')
        self.assertEqual(df['affil_last_country'].dtypes, 'string')
        self.assertEqual(df['affil_fill_country'].dtypes, 'string')
        self.assertEqual(df['countries_lc'].dtypes, 'category')
        self.assertEqual(df['lmic_author_flag'].dtypes, 'bool')
        self.assertEqual(df['lmic_author_lower_flag'].dtypes, 'bool')
        self.assertEqual(df['lmic_china_flag'].dtypes, 'bool')



if __name__ == '__main__':
    unittest.main()