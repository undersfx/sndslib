# SNDS LIB

A personal project to process and verify data from SNDS panels more easily.

Simple Usage:

	>>>import sndslib
	>>>r = sndslib.getipstatus('mykey')
	>>>ips = sndslib.lista(r)
	>>>print('\n'.join(ips))
      
More information in the [SNDS](https://sendersupport.olc.protection.outlook.com/snds/FAQ.aspx?wa=wsignin1.0) and [SNDS Automated Data Access](https://sendersupport.olc.protection.outlook.com/snds/auto.aspx) pages.
