"""
Company: Eutility
Author: Ricky
Version: 1.1
Date"4/08/2016

"""

from pyPdf import PdfFileReader, PdfFileWriter
from random import randint
import time
import inspect, os
import StringIO
import re

class PDF:
	def __init__(self, file_name):
		self.old_name = file_name
		self.pageNum = 0
		self.content = None
		self.new_name = None
    
def CurrentPath():
        # Identify current python files location
        
	path =  os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))  #get current path
	return path + "\\"

retailers = ['AGL', 'Origin', 'Momentum', 'ERM', 'Alinta', 'EA']
AGL = ['NMI[]Supply period']      #NMI20010049300Supply period11 Jan 2016  to 12 Jan 2016 ( 2days)
PATH = CurrentPath()

def TimeStamp():
        #return the date that this code been excuted. format ddmmYYY -> e.g. 170602016
        return time.strftime("%d%m%Y%H%M%S")


def StripTime_Month(mth):
        # convert Jun to 7
        if 'Jan' in mth:
                return 1
        if 'Feb' in mth:
                return 2
        if 'Mar' in mth:
                return 3
        if 'Apr' in mth:
                return 4
        if 'May' in mth:
                return 5
        if 'Jun' in mth:
                return 6
        if 'Jul' in mth:
                return 7
        if 'Aug' in mth:
                return 8
        if 'Sep' in mth:
                return 9
        if 'Oct' in mth:
                return 10
        if 'Nov' in mth:
                return 11
        if 'Dec' in mth:
                return 12
        #unrecognise value
        return False

def ConvertDate(date, retailer):
        #convert string into num string, e.g. 11 Jun 2015 -> 11072015
        postfix = "_the-starting-date-is-incorrect" #use it to indicate start date is non 1st
        if retailer == 'AGL':
                i_mth = 1  #index for month position
                date_List = date.split('to')
                start_date = date_List[0].strip()
                date_elem = start_date.split()
                mth = StripTime_Month(date_elem[i_mth])
                if mth:
                        day = int(date_elem[0])
                        if day != 1:
                                return str(mth).zfill(2) + "-" + date_elem[2].zfill(4) + postfix
                        return str(mth).zfill(2) + "-" + date_elem[2].zfill(4)
                return False

def Find_NMI_Date(content):
        if "AGL" in content:
                retailer = "AGL"
                meter_type = ""
                #electricity invoice
                if "NMI" in content:
                        meter_type = "NMI"

                #gas invoice
                if "MIRN" in content:
                        meter_type = "MIRN"
                        
                regex = r"Your {}(.+)Supply period?".format(meter_type)
                nmi = re.findall(regex, content)
                nmi = nmi[0].strip()[0:10]
                #print nmi

                regex = r"Your {}.+Supply period(.*?)\(".format(meter_type)
                date = re.findall(regex, content)
                date = date[0].strip()
                date = ConvertDate(date, retailer)
                #print date
        #combine all
        return nmi + "_" + date
        
                
        

def main():
        start_time = time.time()
        count = 0
        pdf_list = GetAllPDF()  # get the name list of all pdf files in current location
        for i in pdf_list:
                count +=1
                print count, "Excuting PDF:", i.old_name
                #get content
                content = GetPDFContent(i.old_name)
                #check retailer:
                #print content
                #identify retailer
                
                new_name = Find_NMI_Date(content)

                #rename
                try:
                        #print "change name from", i.old_name, "to ", new_name
                        new_name = new_name + ".pdf"
                        old_name = i.old_name
                        RenameFile(old_name, new_name)                        
                        
                except:
                        print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Error at: old name- new name:", new_name
                        # if file is open
                #print "New name>>", new_name
                print " "
        print("--- %s seconds ---" % (time.time() - start_time))
def GetPDFContent(fileName):
        """
        open the pdf and return the content
        """
        content = ""

        with file(PATH + fileName, "rb") as p:
                pdf = PdfFileReader(p)
                num_pages = GetPDFpagesNumbers(fileName)

                for i in range(0, num_pages):
                        content += pdf.getPage(i).extractText()
                        #print 'excuteing page:', i

        return content

def GetPDFpagesNumbers(fileName):
        """
        open the pdf file and return the total page number
        sample path: C:/Users/rfzheng/Desktop/
        sample file name: 123.pdf

        """
        num = 2 #by default
        with open(PATH + fileName, 'rb') as f:
            pdf = PdfFileReader(f)
            num = pdf.getNumPages()
            #print num
        return num
    
    


def RenameFile(old_name, new_name):

        postfix = ".pdf"
        new_name = new_name + postfix
        
        for filename in os.listdir(PATH):
                if filename.startswith(old_name):
                        if NameCheck(new_name):
                                pass
                                #print "Error: duplicated name- new name:", new_name
                        os.rename(filename, new_name)
                        #print "!!!Successful"




def GetAllPDF(fileType = '.pdf'):
        pdf_list = []
        for f in os.listdir(PATH):
                filename, file_extension = os.path.splitext(f)
		#convert upper case to lower case, e.g. .PDF -> .pdf
                file_extension = file_extension.lower()
                if file_extension == fileType:
                        pdf_item = PDF(f)
                        pdf_list.append(pdf_item)
        return pdf_list

def NameCheck(name):
        #check if duplicate name
        duplicate_msg = "_duplicatedFile_"
        pdf_list = GetAllPDF()
        
        for i in pdf_list:
                if name == i.old_name:
                        return duplicate_msg + name + TimeStamp() + "_" + str(randint(1000,9999))


if __name__ == '__main__':
        main()
