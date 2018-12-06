import-module activedirectory 
 Get-ADUser -Filter ('manager -eq "extpmh"')|foreach { $_.SamAccountName }