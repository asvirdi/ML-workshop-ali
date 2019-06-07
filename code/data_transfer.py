import elasticsearch5
import elasticsearch5.helpers
import logging
import urllib3


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)






logger = logging.getLogger('data_transfer_module')
logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s')
logger.setLevel(logging.DEBUG)


index='kddcup-data'
elasitcUsername = 'SKFT0SRVsaifgESread'
elasticPassword = ''





def connect_to_elastic():
    logger.info(msg='connecting to elastic')
    connection_string = 'https://' + elasitcUsername + ':' + elasticPassword + '@' + '155fd9b2b64f446894e2a6d5f1286a2f.ece.saifg.rbc.com' + ':' + '9243'
    es = elasticsearch5.Elasticsearch([connection_string], use_ssl=False, verify_certs=False, timeout=600)
    return es



def get_data_from_elastic(index):
    es = connect_to_elastic()
    try:
        logger.info(msg='scanning elastic for data..')
        res = elasticsearch5.helpers.scan(client=es, query={"query":{"match_all":{}}}, index=index, doc_type="json")
        output  =  [ item['_source'] for item in res]
        logger.warning(msg='returing output from elastic')
        return output

    except Exception as e:
        print('Error happened in running a search query on index {}!'.format(index))
        print(e)
        return -1


def main():
    get_data_from_elastic(index)

if __name__=="__main__":
    main()