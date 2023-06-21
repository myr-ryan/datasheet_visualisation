import unittest
from Plot_Data import *

class TestData(unittest.TestCase):
    empty_data = {'x':[],'y':[]}
    plot_data = Plot_Data(empty_data)

    # The link for excel should be customized
    f = '/Users/ryanma/Library/CloudStorage/OneDrive-King\'sCollegeLondon/kings/Datasheet.xlsx'
    df_temp = pd.read_excel(f, sheet_name='Sheet1', engine='openpyxl')
    plot_data.upload_data(df_temp)
    plot_data.preprocessing()


    def test_list_in_plotdata(self):

        # print(plot_data.brackets_list)

        self.assertEqual(self.plot_data.brackets_list, ['image_size', 'augmentation_techniques', 'explainability', 'balanced_techniques', 'dataset_pretrained', 'neural_network_type', 
                                                   'data_collection_technology', 'authors', 'author_affils', 'keywords', 'mesh_terms', 'references_pmids', 
                                                   'affil_countries', 'affil_countries_unique', 'countries_lc', 'task', 'subspec'])

    
    def test_data_type(self):

        # empty_data = {'x':[],'y':[]}
        # plot_data = Plot_Data(empty_data)

        # # The link for excel should be customized
        # f = '/Users/ryanma/Library/CloudStorage/OneDrive-King\'sCollegeLondon/kings/Datasheet.xlsx'
        # df_temp = pd.read_excel(f, sheet_name='Sheet1', engine='openpyxl')
        # plot_data.upload_data(df_temp)
        # plot_data.preprocessing()

        df = pd.DataFrame(self.plot_data.source.data)
        self.assertEqual(df['task'].dtypes, 'category')
        self.assertEqual(df['subspec'].dtypes, 'category')
        self.assertEqual(df['Paper_ID'].dtypes, 'int')
        self.assertEqual(df['Title'].dtypes, 'string')
        self.assertEqual(df['ml_task_description'].dtypes, 'category')
        self.assertEqual(df['patient_num'].dtypes, 'float')
        self.assertEqual(df['image_size'].dtypes, 'category')
        self.assertEqual(df['image_type'].dtypes, 'category')
        self.assertEqual(df['augmentation_used'].dtypes, 'bool')
        self.assertEqual(df['augmentation_techniques'].dtypes, 'category')
        self.assertEqual(df['data_augmented'].dtypes, 'bool')
        self.assertEqual(df['DataSize_all'].dtypes, 'float')
        self.assertEqual(df['DataSize_validation'].dtypes, 'float')
        self.assertEqual(df['DataSize_testing'].dtypes, 'float')
        self.assertEqual(df['DataSize_training'].dtypes, 'float')
        self.assertEqual(df['explainability'].dtypes, 'category')
        self.assertEqual(df['balanced'].dtypes, 'bool')
        self.assertEqual(df['balanced_comment'].dtypes, 'string')
        self.assertEqual(df['balanced_techniques'].dtypes, 'category')
        self.assertEqual(df['bias'].dtypes, 'string')
        self.assertEqual(df['class_labels'].dtypes, 'string')
        self.assertEqual(df['data_source'].dtypes, 'string')
        self.assertEqual(df['data_links'].dtypes, 'string')
        self.assertEqual(df['raw_data_availability'].dtypes, 'category')
        self.assertEqual(df['processed_data_availability'].dtypes, 'category')
        self.assertEqual(df['code_availability'].dtypes, 'bool')
        self.assertEqual(df['code_links'].dtypes, 'string')
        self.assertEqual(df['gender'].dtypes, 'category')
        self.assertEqual(df['age_specified'].dtypes, 'string')

        # self.assertEqual(df['task_seg+obj_det'].dtypes, 'bool')
        # self.assertEqual(df['task_detection'].dtypes, 'bool')
        # self.assertEqual(df['task_diagnosis'].dtypes, 'bool')
        # self.assertEqual(df['task_prognosis'].dtypes, 'bool')
        # self.assertEqual(df['task_treatment_design'].dtypes, 'bool')
        self.assertEqual(df['treatment_design_comment'].dtypes, 'string')
        # self.assertEqual(df['task_risk prediction'].dtypes, 'bool')
        self.assertEqual(df['risk_prediction_comment'].dtypes, 'string')
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
        self.assertEqual(df['dataset_pretrained'].dtypes, 'category')
        self.assertEqual(df['neural_network_type'].dtypes, 'category')
        self.assertEqual(df['data_collection_technology'].dtypes, 'category')
        self.assertEqual(df['algorithm_pipeline'].dtypes, 'string')
        self.assertEqual(df['comments'].dtypes, 'string')
        self.assertEqual(df['year'].dtypes, 'datetime64[ns]')
        self.assertEqual(df['algo_neural_net'].dtypes, 'bool')
        self.assertEqual(df['ID'].dtypes, 'int')
        self.assertEqual(df['pmid'].dtypes, 'int')
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
        self.assertEqual(df['mesh_terms'].dtypes, 'category')
        self.assertEqual(df['references_pmids'].dtypes, 'category')
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