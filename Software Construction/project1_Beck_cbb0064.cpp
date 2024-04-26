/*Cameron Beck
 *CBB0064
 *project1_Beck_cbb0064.cpp
 *To compile this code use the g++ command.
 */
 
#include <iostream>
using namespace std;

int main() {

double interestRate,interestRateC,monthlyPaid,interestTotal=0;
int loan,currentMonth=0;
// VARIABLE INITIALIZATION
// CURRENCY FORMATTING
cout.setf(ios ::fixed);
cout.setf(ios ::showpoint);
cout.precision(2);

// USER INPUT
// NOTE: For valid input, the loan, interest, and monthly payment must
// be positive. The monthly payment must also be large enough to
// terminate the loan.

while(true) {
cout << "\nLoan Amount: ";
cin >> loan;

if(loan>0) {
break;
}
else {
cout<<"Loan must be positive.\n";
}
}
while(true){
cout << "Interest Rate (% per year): ";
cin >> interestRate;
if(interestRate>0) {
break;
}
else{
cout<<"Interest rate must be positive.\n";
}
}

// GET PROPER INTEREST RATES FOR CALCULATIONS
interestRate /= 12;
interestRateC = interestRate / 100;
while(true){
cout << "Monthly Payments: ";
cin >> monthlyPaid;
if(monthlyPaid<loan){
break;
}
else{
cout<<"Monthly payment must be less than loan amount.\n";
}
}


cout << endl;

// AMORTIZATION TABLE
cout << "*****************************************************************\n"
<< "\tAmortization Table\n"
<< "*****************************************************************\n"
<< "Month\tBalance\t\tPayment\tRate\tInterest\tPrincipal\n";

// LOOP TO FILL TABLE
while (loan > 0) {
if (currentMonth == 0) {
cout << currentMonth++ << "\t$"<< loan;
if (loan < 1000) cout << "\t" ; 
cout << "\t" << "N/A\tN/A\tN/A\t\tN/A\n";
}
if (monthlyPaid > loan) {
cout<<currentMonth++ <<"\t$" ;
double interestAmt=loan*(interestRateC);
monthlyPaid = loan + interestAmt;  
interestTotal+=interestAmt;
loan=0;
cout<<loan;
cout<<"\t\t";

cout<<"$";
cout<<monthlyPaid<<"\t";

cout<<interestRate<<"%\t$";
cout<<interestAmt<<"\t\t$";
//loan-=(monthlyPaid-interestAmt);
cout<<(monthlyPaid-interestAmt)<<"\n";

}
else {

cout<<currentMonth++ <<"\t$";
double interestAmt=loan*(interestRateC);
interestTotal+=interestAmt;
loan-=(monthlyPaid-interestAmt);
cout<<loan;

if (loan < 1000) cout << "\t" ;
cout<<"\t";

cout<<"$";
cout<<monthlyPaid<<"\t";

cout<<interestRate<<"%\t$";
cout<<interestAmt<<"\t\t$";
//loan-=(monthlyPaid-interestAmt);
cout<<(monthlyPaid-interestAmt)<<"\n";

/* Properly calculate and display “montlypaid” and “principal” when
(1) loan * (1 + interestRateC) < monthlyPaid
and (2) loan * (1 + interestRateC) >= monthlyPaid
*/
}
}


cout << "****************************************************************\n";
cout << "\nIt takes " << -- currentMonth << " months to pay off "
<< "the loan.\n"
<< "Total interest paid is: $" << interestTotal;
cout << endl << endl;
return 0;
}
