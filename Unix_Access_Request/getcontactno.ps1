import-module activedirectory 
 Get-ADUser -Id extpmh -Properties *|  foreach { $_.mobile }