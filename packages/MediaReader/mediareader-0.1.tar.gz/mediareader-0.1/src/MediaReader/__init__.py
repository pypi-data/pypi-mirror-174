class mediaReader():
    def __init__(self, readerPlan , s3 ): 
        
        self.readerPlan = readerPlan
        self.s3r = s3['s3r']
        self.s3c = s3['s3c']
        self.readerBucket = s3['bucketName']
        self.factorBucket = s3['factorBucket']
