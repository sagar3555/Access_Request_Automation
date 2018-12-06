param ($requestername)
Get-ADUser $requestername | foreach { $_.UserPrincipalName }
(get-aduser (get-aduser $requestername -Properties manager).manager).samaccountName 
(Get-AdUser (Get-aduser $requestername -properties manager).manager -properties emailaddress).EmailAddress