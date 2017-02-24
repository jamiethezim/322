import sys
from urllib.request import Request, urlopen
from urllib.parse import urlencode

#Usage: python3 revoke_user.py <URL> <username>
def main():
	#check arguments
	if len(sys.argv) < 3:
		print("Usage: python3 %s <URL> <username>"%sys.argv[0])
		return None

	#prepare the request
	args = {'username': sys.argv[2]}

	#Package the request
	data = urlencode(args)
	#Make the request
	req = Request(sys.argv[1]+'revoke_user', data.encode('ascii'), method='POST')
	res = urlopen(req)
	
	recieved = res.read().decode('ascii')
	print(recieved)
if __name__ == '__main__':
	main()
