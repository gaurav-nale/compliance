# Has all the keys and configurations present in the AWS

# AWS S3 bucket configuration
S3_BUCKET_1 = "sdn-compliance"
S3_KEY_1 = "try_consolidated.csv"
S3_BUCKET_2 = ""
S3_KEY_2 = ""

# Aurora DB Configuration
AURORA_HOST = "knowledgebasequickcreateaurora-007-auroradbcluster-nehjn66dsqz7.cluster-ctc0s4my8k73.us-east-2.rds.amazonaws.com"
AURORA_PORT = 5432
AURORA_DATABASE = "Bedrock_Knowledge_Base_Cluster"
AURORA_USER = "gaurav.nale"
AURORA_PASSWORD = "gabbU@2696"
VECTOR_TABLE = "bedrock_integration.bedrock_knowledge_base"
VECTOR_COLUMN = "embedding"
TEXT_COLUMN = ""
ID_COLUMN = ""

# AWS Bedrock Knowledge Base Configuration
KNOWLEDGE_BASE_ID = ""
DATA_SOURCE_ID = ""
EMBEDDING_MODEL_ARN = ""