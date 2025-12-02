function toggleAssetDetailTabs(executionContext) {
    // Get the form context for the modern API access
    var formContext = executionContext.getFormContext();

    // --- Configuration (Based on your input) ---
    var classificationFieldName = "crd3b_assetclassification"; 
    
    // Internal names for the tabs - CONFIRM THESE MATCH YOUR FORM
    var fundTabName = "tab_fund_details"; // Example name
    var loanTabName = "tab_loan_details"; // Example name
    var coInvestDebtTabName = "tab_coinvest_debt_details"; // Example name
    var coInvestEquityTabName = "tab_coinvest_equity_details"; // Example name
    
    // Integer values for the Choice options (0, 1, 2, 3)
    var FUND_VALUE = 0; 
    var LOAN_VALUE = 1; 
    var COINVEST_DEBT_VALUE = 2;
    var COINVEST_EQUITY_VALUE = 3;
    // ---------------------------------------------
    
    var classificationAttribute = formContext.getAttribute(classificationFieldName);
    var classificationValue = (classificationAttribute) ? classificationAttribute.getValue() : null;

    // Get Tab controls
    var fundTab = formContext.ui.tabs.get(fundTabName);
    var loanTab = formContext.ui.tabs.get(loanTabName);
    var coInvestDebtTab = formContext.ui.tabs.get(coInvestDebtTabName);
    var coInvestEquityTab = formContext.ui.tabs.get(coInvestEquityTabName);
    
    // Hide all detail tabs initially
    var detailTabs = [fundTab, loanTab, coInvestDebtTab, coInvestEquityTab]; 
    detailTabs.forEach(function(tab) {
        if (tab) {
            tab.setVisible(false);
        }
    });

    // Show the relevant tab and set focus
    if (classificationValue !== null) {
        switch (classificationValue) {
            case FUND_VALUE:
                if (fundTab) {
                    fundTab.setVisible(true);
                    fundTab.setFocus(); // 🖱️ THIS IS THE CRITICAL LINE
                }
                break;
            case LOAN_VALUE: 
                if (loanTab) {
                    loanTab.setVisible(true);
                    loanTab.setFocus();
                }
                break;
            case COINVEST_DEBT_VALUE:
                if (coInvestDebtTab) {
                    coInvestDebtTab.setVisible(true);
                    coInvestDebtTab.setFocus();
                }
                break;
            case COINVEST_EQUITY_VALUE:
                if (coInvestEquityTab) {
                    coInvestEquityTab.setVisible(true);
                    coInvestEquityTab.setFocus();
                }
                break;
        }
    }
}