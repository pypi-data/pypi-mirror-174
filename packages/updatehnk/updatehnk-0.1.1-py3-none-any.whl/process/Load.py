import process.util as util
import process.fields as field
from google.cloud import bigquery


class Load:
    def __init__(self,
                 config: dict
                 ):
        super(Load, self).__init__()
        self.config = config
        self.tmp_table_name = util.get_tmp_table_name(config=self.config)
        self.tmp_config = (self.tmp_table_name, field.FIELDS_TMP_BQ, self.config)
        self.tmp_table_structure = util.get_bq_temp_table_def(config=self.tmp_config)
        self.avro_filename_from_bucket = util.get_last_avro_filename_from_bucket(config=self.config)
        self.query_heineken_merge_context = util.query_heineken_upsert(tmp_table_name=self.tmp_table_name)
        self.query_erp_merge_context = util.query_erp_upsert()

    def upsert(self):
        util.create_bq_tmp_table(client=bigquery.Client, tmp_table=self.tmp_table_structure)
        util.job_avro_load_to_bq_tmp_table(client=bigquery.Client,
                                           temp_table_name=self.tmp_table_name,
                                           file_path=self.config['file_path'],
                                           file_name=self.avro_filename_from_bucket)

        util.bq_exec_query(client=bigquery.Client,
                           query=self.query_heineken_merge_context,
                           src='merge_heineken_temp_table')

        util.bq_exec_query(client=bigquery.Client,
                           query=self.query_erp_merge_context,
                           src='merge_external_query_erp')