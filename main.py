from curr_database import CurrencyDatabase

if __name__ == "__main__":

  # Params
  db_start_date = (1, 4, 2018)
  db_end_date = (30, 6, 2018)
  trigger_list_path = "./triggers.txt"

  # Database Constructor
  tcmb = CurrencyDatabase(db_start_date,db_end_date)

  # Analysis
  tcmb.analyze(trigger_list_path, debug=True)