import-module activedirectory 
get-aduser -filter{samaccountname -eq 'H00DSN'} -properties mail | Select -expandproperty mail