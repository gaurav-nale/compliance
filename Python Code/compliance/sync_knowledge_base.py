import boto3

def sync_knowledge_base(knowledge_base_id, data_source_id):
    try:
        bedrock_client = boto3.client(
            service_name = "bedrock-agent",
            region_name = "us-east-2",
            aws_access_key_id='ASIA3FLD26ANOVSBDW6O', 
            aws_secret_access_key='XD7J/jCAN8Wj3r0+Xhizb+MHHxe3OjjHyeAn3Gt6',
            aws_session_token = 'IQoJb3JpZ2luX2VjEHwaCXVzLWVhc3QtMSJHMEUCIDUrwNRmzR4ie08rv5OrOfDAB5bVcnu/o1XsNqk02NgXAiEAtltpl6988bQ5Nvpg6Pg0OQiP572U8R9ws1EehcplYc4q/AIIxf//////////ARAAGgw3NjczOTc5MTY2OTgiDGnLllT4Rj7KMDA2mSrQAkCgPrJ0CnArRB0A3A7I7v7orpk8LmLa9D+/RIznbdXKOaspXjMbyVC3NenHR5SewGSQbJ29fs+Ft5H02mI44Oudg6dlQ9qNxG8ew1sO2KUeuwrtnpNF5aiO9yfVrYnMlj4owXdKVC1FTFX4BLA2UfvfCbxUsZykDHW6r4nVtMmP30LWcJ7CVTjnPW1ZCQziD+1hHI2f7iAjulMyFH3lDJbCwUVEuosBk7ALr8uBsvkliNRVwMygu9ikKngihW9JtWegLa5e8PbB4m9B4zCW9yT4nAQr3A4hPVY3UThKoDMZNfg7uAFzO157Khzz61p2jrWGV7R6Wmde3wnih7LRy3q09CpFWNXWCU5DfeRe5N/QcPdY6wI17y+i6nTCNZVa//WUCp81kiup67X4w2dsRhr8X9xXvFxC81VXC9quusRORAZRDnYoyWTeXc5BNiHdfTDuxse+BjqnAS78nvZxMYiheD9t6fqH2GRUvukD6XvwtquWYovddLNztlu5EhrbhED/oMeuWam9VCDC/hXOeqqEerYFplERntzmaGMLDw+jgeZx1DiijcAhucA6LBgAfMGpG6+qo82I2dL5sRI2DJK2epECE1cSFGyVIE/EBaSUoKVfyGfa1YBYnOEJb31qRYVM06V73FyJWppCFMNZtmaAEBHOxs8sBiZyjdUrHSCZ'
        )

        response = bedrock_client.start_ingestion_job(
            knowledgeBaseId = knowledge_base_id,
            dataSourceId = data_source_id
        )

        return response

    except Exception as e:
        print(f"Error syncing knowledge base: {e}")
        return None

knowledge_base_id = "EIGVGRJK8W"
data_source_id = "JF381K51TE"

sync_result = sync_knowledge_base(knowledge_base_id, data_source_id)

if sync_result:
    print("Knowledge base synchronization triggered successfully.")

else:
    print("Knowledge base synchronization failed.")