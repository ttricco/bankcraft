account_types = ['chequing', 'saving', 'credit']
banks = ['bank_1', 'bank2']
bank_accounts = [[0] * len(account_types)] * len(banks)
for (bank, bank_counter) in zip(banks, range(len(banks))):
    for (account_type, account_counter) in zip(account_types, range(len(account_types))):
        bank_accounts[bank_counter][account_counter] = account_type


print(bank_accounts)
