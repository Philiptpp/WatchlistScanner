from scanner import Scanner

my_scanner = Scanner('watchlist.txt')
my_scanner.ignore_list = ['doji', 'spinning_top']
my_scanner.scan_watchlist()
