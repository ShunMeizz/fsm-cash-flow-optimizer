# CASH FLOW OPTIMIZER

    The Cash Flow Statement is a key part of the Financial Statement, tracking a company’s cash activities—both inflows (cash coming in) and outflows (cash going out) over a given period across Operating (CFO), Investing (CFI), and Financing (CFF) activities.

    The goal is to guide users through states to ensure an **overall Cash Inflow**, helping businesses identify shortages and redirect resources effectively.
    Since there are many operating, investing, and financing activities, I have classified them into two major groups: those that cause Inflow and those that cause Outflow.

    Classification
    i. Under CFO (Operating Activities)
        1. Cash Receipt (can lead to Inflow): eg. Cash Sales
        2. Cash Payment (can lead to Outflow): eg. Pay for employees, Rent Payment
    ii. Under CFI (Investing Activities)
        3. Asset Sale (can lead to Inflow): eg. Sale of Equipment, Sale of Investment
        4. Asset Purchase (can lead to Outflow) eg. Purchase of Equipment, Construction of Building
    iii. Under CFF (Financing Activities)
        5. Loan/Share Issue (can lead to Inflow) e.g. Loan Acquisition, Issuance of Shares
        6. Loan Repayment (can lead to Outflow) e.g. Repayment of Loans/Borrowings

### States

q0- Initial State
q1- CFO Inflow >= Outflow
q2- CFO Inflow < Outflow
q3- CFI Inflow >= Outflow
q4- CFI Inflow < Outflow
q5- CFF Inflow >= Outflow
q6- CFF Inflow < Outflow
q7- Final State (Overall: INFLOW)

### Transition Table

+------+----------------------+-----------------------+
| State| Inflow | Outflow |
+------+----------------------+-----------------------+
| q0 | ['q1'] | ['q2'] |
| q1 | ['q3'] | ['q1', 'q2'] |
| q2 | ['q3', 'q5'] | ['q2'] |
| q3 | ['q5'] | ['q3', 'q4'] |
| q4 | ['q1', 'q5'] | ['q4'] |
| q5 | ['q7'] | ['q5', 'q6'] |
| q6 | ['q1', 'q3'] | ['q6'] |
| q7 | ['q7'] | [] |
+------+----------------------+-----------------------+

### PS: Inflow/Outflow, Deficit/Surplus (same same)
