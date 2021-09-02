# instaSpy
The project is intended to spy on accounts, in a way that takes data from followers and follows and compares with information from different dates.

#use 
- Copy `.env.example` to `.env` and set values.
- `pip install -r requirements.txt`
- Run `python -m smtpd -c DebuggingServer -n localhost:1025` on prompt.
- Run  `initial.py` once a day, when have data of two days or more, execute `calculate.py` for calculate diferences into data.