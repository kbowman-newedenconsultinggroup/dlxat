#DISM /Online /Add-Capability /CapabilityName:WMIC

mkdir c:\tckc

wmic product >> c:\tckc\software.log

wmic product where "name='HP Wolf Security'" call uninstall
wmic product where "name='HP Wolf Security - Console'" call uninstall
wmic product where "name='HP Wolf Security Application Support for Chrome 138.0.7204.170'" call uninstall
wmic product where "name='HP Security Update Service'" call uninstall
wmic product where "name='HP Wolf Security Application Support for Sure Sense'" call uninstall
wmic product where "name='HP Sure Recover'" call uninstall
wmic product where "name='HP Sure Run Module'" call uninstall
wmic product where "name='Office 16 Click-to-Run Extensibility Component'" call uninstall
wmic product where "name='Office 16 Click-to-Run Licensing Component'" call uninstall
wmic product where "name='HP System Default Settings'" call uninstall
wmic product where "name='HP Notifications'" call uninstall

wmic product >> c:\tckc\software.log
