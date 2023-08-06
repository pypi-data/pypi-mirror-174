import os

# def saveFrame(frame, name):
#     frame.to_csv('/Users/Ace/code/dp/jupyter/outputs/' + name + '.csv')
#
# def saveFrameJson(frame, name):
#     row_no = 0
#     with open ("/Users/Ace/code/dp/jupyter/outputs/" + name + ".json", "w") as f:
#         f.write("[[")
#         for col in frame.iteritems():
#             row_no += 1
#             lineString = '"' + col[0] + '"'
#             n = col[0]
#             for i, row in frame.iterrows():
#                 if (isinstance(row[n], str)):
#                     lineString = lineString + ',"' + str(row[n]) + '"'
#                 else:
#                     lineString = lineString + ',' + str(row[n])
#             if (row_no > 1):
#                 f.write("],[")
#             f.write(lineString)
#         f.write("]]")

def commit_table(df):
    # dataset_id = os.environ['DATASET']

    print('Uploading your dataframe [STUB CODE]', df)
    # import boto3
    #
    # session = boto3.Session(profile_name='boto3')
    # s3_client = session.client('s3')
    #
    # bucket = 'singer-test'
    #
    # # make sure provided bucket exists or is accesible
    # s3_client.head_bucket(Bucket=bucket)
    #
    # file = '/Users/Ace/code/dp/jupyter/outputs/' + nb_name + '.json'
    #
    # with open(file, "rb") as f:
    #     s3_client.upload_fileobj(f, bucket, '_dashboard/tables/essex/essex_2022/' + nb_name + '.json')
    #     f.close()
    # print("Written " + nb_name + '.json')
