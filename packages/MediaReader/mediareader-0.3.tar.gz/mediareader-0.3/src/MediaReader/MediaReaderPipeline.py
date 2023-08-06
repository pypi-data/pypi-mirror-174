import boto3
import json
import pandas as pd 
from io import StringIO
import datetime as datetime
from datetime import date

class mediaReader():
    def __init__(self, readerPlan , s3 ): 
        
        self.readerPlan = readerPlan
        self.s3r = s3['s3r']
        self.s3c = s3['s3c']
        self.readerBucket = s3['bucketName']
        self.factorBucket = s3['factorBucket']
    
        
        
    def updateVideoGroupFactors(self,ROS):
        
        rosCapacity= json.loads(self.s3r.Object(self.factorBucket,str(datetime.date.today()) + '/' + f'{ROS}/' + 'capacity.json').get()['Body'].read().decode('utf-8'))
        genreMap = json.loads(self.s3r.Object(self.readerBucket,'products/videogroup/genremap.json').get()['Body'].read().decode('utf-8'))
        filterMap = json.loads(self.s3r.Object(self.readerBucket,'products/videogroup/filtermap.json').get()['Body'].read().decode('utf-8'))
        ratingMap = json.loads(self.s3r.Object(self.readerBucket,'products/videogroup/ratingmap.json').get()['Body'].read().decode('utf-8'))
        videoGroupDf= pd.read_csv(StringIO(self.s3c.get_object(Bucket=self.factorBucket, Key=str(datetime.date.today())+ '/videogroups/rawvideogroup.csv')['Body'].read().decode('utf-8') ))
        filterCapacity = {item : (videoGroupDf[videoGroupDf['Video Group ID'].astype(str).str.contains(filterMap[item])]['Net Counted Ads'].sum() + videoGroupDf[videoGroupDf['Video Group ID'].astype(str).str.contains(filterMap[item])]['Historical Unfilled Available'].sum()) / rosCapacity  for item in filterMap.keys()}
        filterDump = [self.s3r.Object(self.factorBucket,f'{str(datetime.date.today())}/{key}/capacity.json').put(Body = json.dumps(value))  for key, value in filterCapacity.items() ]
        genreCapacity = {genreMap[item] : float((videoGroupDf[videoGroupDf['Video Group ID'].astype(str).str.contains(item)]['Net Counted Ads'].sum() + videoGroupDf[videoGroupDf['Video Group ID'].astype(str).str.contains(item)]['Historical Unfilled Available'].sum()) / rosCapacity ) for item in genreMap.keys()}
        genreDump = self.s3r.Object(self.factorBucket,str(datetime.date.today()) + '/genre/capacity.json').put(Body = json.dumps(genreCapacity))
        ratingCapacity = {ratingMap[item] : float((videoGroupDf[videoGroupDf['Video Group ID'].astype(str).str.contains(item)]['Net Counted Ads'].sum() + videoGroupDf[videoGroupDf['Video Group ID'].astype(str).str.contains(item)]['Historical Unfilled Available'].sum()) / rosCapacity ) for item in ratingMap.keys()}
        ratingDump = self.s3r.Object(self.factorBucket,str(datetime.date.today()) + '/rating/capacity.json').put(Body = json.dumps(ratingCapacity))

    def updateSeriesFactors(self,data,ROS):
        
        capacity = json.loads(self.s3r.Object(self.factorBucket,f'{str(datetime.date.today())}/{ROS}/capacity.json').get()['Body'].read().decode('utf-8'))
        df = pd.read_csv(self.s3c.get_object(Bucket= self.factorBucket, Key= f'{str(datetime.date.today())}/{data}/raw{data}.csv') ['Body']) 
        df['Capacity'] = df['Net Counted Ads'] + df['Historical Unfilled Available']
        df['Percent of Capacity'] = [float(item/df['Capacity'].sum())  for item in df['Capacity'] ]
        showDict = {str(df['Series ID'][i]) : df['Percent of Capacity'][i] for i in range(len(df['Percent of Capacity']))}
        capacityPut = self.s3r.Object(self.factorBucket,f'{str(datetime.date.today())}/{data}/series.json' ).put(Body = json.dumps(showDict))
        dataPut = self.s3r.Object(self.factorBucket,f'{str(datetime.date.today())}/{data}/capacity.json' ).put(Body = json.dumps(float(df['Capacity'] .sum()) / capacity))


    def updateSiteGroupFactors(self,data,ROS):
        
        capacity = json.loads(self.s3r.Object(self.factorBucket,f'{str(datetime.date.today())}/{ROS}/capacity.json').get()['Body'].read().decode('utf-8'))
        df = pd.read_csv(self.s3c.get_object(Bucket= self.factorBucket, Key= f'{str(datetime.date.today())}/{data}/raw{data}.csv') ['Body']) 
        df['Capacity'] = df['Net Counted Ads'] + df['Historical Unfilled Available']
        df['Percent of Capacity'] = [float(item/df['Capacity'].sum())  for item in df['Capacity'] ]
        showDict = {str(df['Site Group ID'][i]) : df['Percent of Capacity'][i] for i in range(len(df['Percent of Capacity']))}
        capacityPut = self.s3r.Object(self.factorBucket,f'{str(datetime.date.today())}/{data}/series.json' ).put(Body = json.dumps(showDict))
        dataPut = self.s3r.Object(self.factorBucket,f'{str(datetime.date.today())}/{data}/capacity.json' ).put(Body = json.dumps(float(df['Capacity'] .sum()) / capacity))
        
    def getDataMaps(self):
    
        self.siteGroupMap = json.loads(self.s3r.Object(self.readerBucket, 'products/sitegroup/datamap.json').get()['Body'].read().decode('utf-8'))
        self.seriesMap = json.loads(self.s3r.Object(self.readerBucket, 'products/series/datamap.json').get()['Body'].read().decode('utf-8'))

    def updateRosData(self,data):
        
        df = pd.read_csv(self.s3c.get_object(Bucket= self.factorBucket, Key= f'{str(datetime.date.today())}/{data}/raw{data}.csv') ['Body']) 
        df['Capacity'] = df['Net Counted Ads'] + df['Historical Unfilled Available']
        df['Percent of Capacity'] = [float(item/df['Capacity'].sum())  for item in df['Capacity'] ]
        showDict = {str(df['Series ID'][i]) : float(df['Percent of Capacity'][i]) for i in range(len(df['Percent of Capacity']))}
        capacityPut = self.s3r.Object(self.factorBucket,f'{str(datetime.date.today())}/{data}/series.json' ).put(Body = json.dumps(showDict))
        dataPut = self.s3r.Object(self.factorBucket,f'{str(datetime.date.today())}/{data}/capacity.json' ).put(Body = json.dumps(float(df['Capacity'].sum())))
