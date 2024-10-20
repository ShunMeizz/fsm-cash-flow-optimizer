from cash_flow_optimizer import CashFlowOptimizer

def view_statement(optimizer, company_name, statement_start_date, statement_end_date, cash_at_start_year):
    net_cfo = optimizer.surplus['Cash Receipt'] - optimizer.deficit['Cash Payment']
    net_cfi = optimizer.surplus['Asset Sale'] - optimizer.deficit['Asset Purchase']
    net_cff = optimizer.surplus['Loan Share Issue'] - optimizer.deficit['Loan Repayment']

    cash_at_end_year = float(cash_at_start_year) + optimizer.overall_cash_flow


    print(f"""=====================================================
    📊 {company_name} - Cash Flow Statement 🧾
    Period: {statement_start_date} to {statement_end_date}
=====================================================
 1️⃣ Cash Flow From Operating Activities (CFO)
    Cash Receipts: Php {optimizer.surplus['Cash Receipt']:.2f}
    Cash Payments: Php {optimizer.deficit['Cash Payment']:.2f}
    ➡️ NET CASH PROVIDED BY OPERATING ACTIVITIES: Php {net_cfo:.2f}

 2️⃣ Cash Flow From Investing Activities (CFI)
    Asset Sales: Php {optimizer.surplus['Asset Sale']:.2f}
    Asset Payments: Php {optimizer.deficit['Asset Purchase']:.2f}
    ➡️ NET CASH USED BY INVESTING ACTIVITIES: Php {net_cfi:.2f}

 3️⃣ Cash Flow From Financing Activities (CFF)
    Loan/Share Issues: Php {optimizer.surplus['Loan Share Issue']:.2f}
    Loan Repayment: Php {optimizer.deficit['Loan Repayment']:.2f}
    ➡️ NET CASH PROVIDED (USED) BY FINANCING ACTIVITIES: Php {net_cff:.2f}

=====================================================
TOTAL NET CASH: Php {optimizer.overall_cash_flow:.2f}
=====================================================
💰 CASH & CASH EQUIVALENTS AT BEGINNING OF YEAR: Php {cash_at_start_year}
💰 CASH & CASH EQUIVALENTS AT END OF YEAR: Php {cash_at_end_year}
=====================================================""")

def main():
    print("""*******************************************************
    🌍 Welcome to Earth's Cash Flow Optimizer! 🚀
    Powered by a Finite State Machine - NFA.
*******************************************************
Let's get started by gathering a few details about your company.""")

    company_name = input("📋 Company Name: ")
    statement_start_date = input("📅 CF Activities START Date: ")
    statement_end_date = input("📅 CF Activities END Date: ")
    cash_at_start_year = input("💰 Cash & Cash Equivalents at the Start of the Year: ")

    optimizer = CashFlowOptimizer()
    optimizer.cash_flow_loop()

    view_statement(optimizer, company_name, statement_start_date, statement_end_date, cash_at_start_year)

if __name__ == "__main__":
    main()
