__author__ = 'Harold'
import re,urllib2
class Get_public_ip:
    def getip(self):
        try:
            myip = self.visit("http://www.ip138.com/ip2city.asp")
        except:
            myip = "So sorry!!!"
        return myip
    def visit(self,url):
        opener = urllib2.urlopen(url)
        if url == opener.geturl():
            str = opener.read()
        return re.search('d+.d+.d+.d+',str).group(0)
if __name__ == "__main__":
    getmyip = Get_public_ip()
    print getmyip.getip()
