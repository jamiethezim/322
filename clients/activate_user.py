import sys
from urllib.request import Request, urlopen
from urllib.parse import urlencode

#Usage: python3 activate_user.py <URL> <username> <password> <title>
def main():
	#check arguments
	if len(sys.argv) < 5:
		print("Usage: python3 %s <URL> <username> <password> <title>"%sys.argv[0])
		return None

	#prepare the request
	args = dict()
	args['username'] = sys.argv[2]
	args['password'] = sys.argv[3]
	args['title'] = sys.argv[4]

	#Package the request
	data = urlencode(args)
	#Make the request
	req = Request(sys.argv[1]+'activate_user', data.encode('ascii'), method='POST')
	res = urlopen(req)
	
	recieved = res.read().decode('ascii')
	print(recieved)
if __name__ == '__main__':
	main()
