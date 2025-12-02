"""
Comprehensive ticker lists - hundreds of most volatile instruments
"""

def get_all_volatile_tickers():
    """Get comprehensive list of volatile tickers"""
    
    # Major Broad Market ETFs
    major_etfs = [
        'SPY', 'QQQ', 'DIA', 'IWM', 'VTI', 'VOO', 'VEA', 'VWO', 'AGG', 'BND',
        'GLD', 'SLV', 'USO', 'TLT', 'HYG', 'LQD', 'EFA', 'EEM', 'FXI', 'EWJ',
        'VGK', 'VPL', 'VXUS', 'VTEB', 'BNDX', 'VCSH', 'VCIT', 'VCLT', 'VGSH', 'VGIT'
    ]
    
    # Sector ETFs
    sector_etfs = [
        'XLF', 'XLE', 'XLI', 'XLK', 'XLV', 'XLP', 'XLY', 'XLB', 'XLU', 'XLC',
        'XBI', 'XRT', 'XHB', 'XES', 'XOP', 'XME', 'XPH', 'XHS', 'XSW', 'XSD',
        'XWEB', 'XHE', 'XNTK', 'XITK', 'XTN', 'XAR', 'XAP', 'XTL', 'XTH', 'XHS'
    ]
    
    # All Leveraged ETFs (3x)
    leveraged_etfs = [
        # QQQ Leveraged
        'TQQQ', 'SQQQ',
        # SPY Leveraged
        'SPXL', 'SPXS', 'UPRO', 'SPXU',
        # Sector Leveraged
        'SOXL', 'SOXS', 'TECL', 'TECS', 'CURE', 'LABU', 'LABD',
        'FAS', 'FAZ', 'TNA', 'TZA', 'UDOW', 'SDOW', 'UMDD', 'SMDD',
        'URTY', 'SRTY', 'YINN', 'YANG', 'CWEB', 'CHAD',
        # Commodity Leveraged
        'BOIL', 'KOLD', 'GUSH', 'DRIP', 'CORN', 'WEAT', 'UCO', 'SCO',
        'UWT', 'DWT', 'USLV', 'DSLV', 'AGQ', 'ZSL', 'JNUG', 'JDST',
        'NUGT', 'DUST', 'GDXJ', 'GDX', 'SILJ', 'BULZ', 'BERZ'
    ]
    
    # Bitcoin ETFs and Crypto
    bitcoin_etfs = [
        'BITO', 'BITI', 'BTCC', 'BTCO', 'HODL', 'BITB', 'BRRR', 'EZBC',
        'BTCW', 'ARKB', 'IBIT', 'FBTC', 'GBTC', 'ETHE', 'BITQ', 'BLOK',
        'LEGR', 'KOIN', 'RIOT', 'MARA', 'COIN', 'HUT', 'HIVE', 'CAN',
        'BITF', 'ARBK', 'CORZ', 'CIFR', 'WULF', 'IREN', 'CLSK', 'BTBT',
        'MSTR', 'SQ', 'PYPL', 'HOOD', 'SI', 'MARA', 'HUT', 'HIVE'
    ]
    
    # Ethereum Leveraged and Related
    ethereum_related = [
        'ETHE', 'ETHX', 'ETHW', 'ETHO', 'ETHE'
    ]
    
    # ARK and Thematic ETFs
    ark_etfs = ['ARKK', 'ARKQ', 'ARKG', 'ARKW', 'ARKF', 'ARKX']
    thematic_etfs = [
        'ROBO', 'BOTZ', 'IRBO', 'QTEC', 'IGV', 'IGM', 'IGE', 'IGF',
        'SKYY', 'HACK', 'FINX', 'SOCL', 'FDN', 'IBUY', 'IBB', 'XBI',
        'IBB', 'XBI', 'IHI', 'IHF', 'IHE', 'IYT', 'IYZ', 'IYW'
    ]
    
    # Volatile Tech Stocks
    volatile_tech = [
        'TSLA', 'NVDA', 'AMD', 'MRNA', 'PLTR', 'RBLX', 'HOOD', 'SOFI',
        'UPST', 'LCID', 'RIVN', 'NIO', 'XPEV', 'LI', 'F', 'RIDE',
        'SPCE', 'ASTS', 'OPEN', 'WISH', 'CLOV', 'SPRT', 'SNDL', 'TLRY',
        'AFRM', 'COIN', 'SQ', 'PYPL', 'SHOP', 'SNOW', 'DDOG', 'NET',
        'ZS', 'CRWD', 'OKTA', 'DOCN', 'ESTC', 'ASAN', 'ZM', 'PTON',
        'FROG', 'MDB', 'MNDY', 'BILL', 'RPD', 'DOCN', 'ESTC', 'ASAN',
        'ZM', 'PTON', 'FROG', 'DDOG', 'NET', 'ZS', 'CRWD', 'OKTA',
        'APP', 'APPN', 'ASAN', 'AVPT', 'BILL', 'BL', 'BSY', 'CFLT',
        'DOCN', 'ESTC', 'FROG', 'FSLY', 'GTLB', 'MDB', 'MNDY', 'NET',
        'NOW', 'OKTA', 'PCTY', 'RPD', 'TEAM', 'VEEV', 'WK', 'ZEN',
        'ZS', 'CRWD', 'DOCN', 'ESTC', 'ASAN', 'ZM', 'PTON', 'FROG'
    ]
    
    # Meme Stocks
    meme_stocks = [
        'GME', 'AMC', 'BB', 'NOK', 'SNDL', 'EXPR', 'NAKD', 'KOSS',
        'BBBY', 'CLOV', 'WISH', 'SPRT', 'TLRY', 'ACB', 'CGC', 'APHA',
        'HEXO', 'OGI', 'CRON', 'SNDL', 'ACB', 'CGC', 'TLRY', 'APHA'
    ]
    
    # Growth Stocks
    growth_stocks = [
        'AAPL', 'MSFT', 'GOOGL', 'GOOG', 'AMZN', 'META', 'NFLX',
        'SNOW', 'DDOG', 'NET', 'ZS', 'CRWD', 'OKTA', 'DOCN', 'ESTC',
        'MDB', 'MNDY', 'BILL', 'RPD', 'FROG', 'DOCN', 'ESTC', 'ASAN',
        'ZM', 'PTON', 'FROG', 'DDOG', 'NET', 'ZS', 'CRWD', 'OKTA',
        'APP', 'APPN', 'ASAN', 'AVPT', 'BILL', 'BL', 'BSY', 'CFLT'
    ]
    
    # Biotech Volatile
    biotech_volatile = [
        'MRNA', 'BNTX', 'NVAX', 'GILD', 'REGN', 'VRTX', 'BIIB', 'ALNY',
        'IONS', 'FOLD', 'ARWR', 'SGMO', 'BEAM', 'CRSP', 'NTLA', 'EDIT',
        'BLUE', 'RGNX', 'RARE', 'FOLD', 'ARWR', 'SGMO', 'BEAM', 'CRSP',
        'NTLA', 'EDIT', 'BLUE', 'RGNX', 'RARE', 'IONS', 'FOLD', 'ARWR',
        'SGMO', 'BEAM', 'CRSP', 'NTLA', 'EDIT', 'BLUE', 'RGNX', 'RARE'
    ]
    
    # Small Cap Volatile
    small_cap_volatile = [
        'SPCE', 'ASTS', 'OPEN', 'WISH', 'CLOV', 'SPRT', 'SNDL', 'TLRY',
        'AFRM', 'COIN', 'SQ', 'PYPL', 'SHOP', 'SNOW', 'DDOG', 'NET',
        'ZS', 'CRWD', 'OKTA', 'DOCN', 'ESTC', 'ASAN', 'ZM', 'PTON',
        'FROG', 'MDB', 'MNDY', 'BILL', 'RPD', 'DOCN', 'ESTC', 'ASAN'
    ]
    
    # Crypto Mining Stocks
    crypto_mining = [
        'RIOT', 'MARA', 'HUT', 'HIVE', 'CAN', 'BITF', 'ARBK', 'CORZ',
        'CIFR', 'WULF', 'IREN', 'CLSK', 'BTBT', 'MSTR', 'HUT', 'HIVE',
        'CAN', 'BITF', 'ARBK', 'CORZ', 'CIFR', 'WULF', 'IREN', 'CLSK'
    ]
    
    # EV Stocks
    ev_stocks = [
        'TSLA', 'LCID', 'RIVN', 'NIO', 'XPEV', 'LI', 'F', 'RIDE',
        'F', 'RIDE', 'LCID', 'RIVN', 'NIO', 'XPEV', 'LI', 'F'
    ]
    
    # Add hundreds more volatile tickers
    # Additional high-volatility stocks
    more_volatile = [
        'AMC', 'GME', 'BB', 'NOK', 'EXPR', 'NAKD', 'KOSS', 'BBBY',
        'SPCE', 'ASTS', 'OPEN', 'WISH', 'CLOV', 'SPRT', 'SNDL', 'TLRY',
        'AFRM', 'COIN', 'SQ', 'PYPL', 'SHOP', 'SNOW', 'DDOG', 'NET',
        'ZS', 'CRWD', 'OKTA', 'DOCN', 'ESTC', 'ASAN', 'ZM', 'PTON',
        'FROG', 'MDB', 'MNDY', 'BILL', 'RPD', 'APP', 'APPN', 'AVPT',
        'BL', 'BSY', 'CFLT', 'FSLY', 'GTLB', 'NOW', 'PCTY', 'TEAM',
        'VEEV', 'WK', 'ZEN', 'RPD', 'FROG', 'DOCN', 'ESTC', 'ASAN'
    ]
    
    # More tech stocks
    more_tech = [
        'AAPL', 'MSFT', 'GOOGL', 'GOOG', 'AMZN', 'META', 'NFLX', 'TSLA',
        'NVDA', 'AMD', 'INTC', 'AVGO', 'QCOM', 'TXN', 'MRVL', 'SWKS',
        'MCHP', 'NXPI', 'ON', 'WOLF', 'DIOD', 'ALGM', 'SLAB', 'CRUS',
        'OLED', 'POWI', 'SITM', 'AMBA', 'LSCC', 'MPWR', 'ALGM', 'SLAB'
    ]
    
    # More biotech/pharma
    more_biotech = [
        'MRNA', 'BNTX', 'NVAX', 'GILD', 'REGN', 'VRTX', 'BIIB', 'ALNY',
        'IONS', 'FOLD', 'ARWR', 'SGMO', 'BEAM', 'CRSP', 'NTLA', 'EDIT',
        'BLUE', 'RGNX', 'RARE', 'FOLD', 'ARWR', 'SGMO', 'BEAM', 'CRSP',
        'NTLA', 'EDIT', 'BLUE', 'RGNX', 'RARE', 'IONS', 'FOLD', 'ARWR',
        'SGMO', 'BEAM', 'CRSP', 'NTLA', 'EDIT', 'BLUE', 'RGNX', 'RARE',
        'ILMN', 'PACB', 'OMCL', 'TECH', 'TMO', 'DHR', 'A', 'BRKR',
        'WAT', 'PKI', 'ICHR', 'NVCR', 'EXAS', 'NEO', 'GH', 'TDOC'
    ]
    
    # More small cap volatile
    more_small_cap = [
        'SPCE', 'ASTS', 'OPEN', 'WISH', 'CLOV', 'SPRT', 'SNDL', 'TLRY',
        'AFRM', 'COIN', 'SQ', 'PYPL', 'SHOP', 'SNOW', 'DDOG', 'NET',
        'ZS', 'CRWD', 'OKTA', 'DOCN', 'ESTC', 'ASAN', 'ZM', 'PTON',
        'FROG', 'MDB', 'MNDY', 'BILL', 'RPD', 'APP', 'APPN', 'AVPT',
        'BL', 'BSY', 'CFLT', 'FSLY', 'GTLB', 'NOW', 'PCTY', 'TEAM',
        'VEEV', 'WK', 'ZEN', 'RPD', 'FROG', 'DOCN', 'ESTC', 'ASAN',
        'AI', 'BBAI', 'SOUN', 'PLTR', 'C3AI', 'PATH', 'U', 'RPD'
    ]
    
    # More crypto-related
    more_crypto = [
        'RIOT', 'MARA', 'HUT', 'HIVE', 'CAN', 'BITF', 'ARBK', 'CORZ',
        'CIFR', 'WULF', 'IREN', 'CLSK', 'BTBT', 'MSTR', 'HUT', 'HIVE',
        'CAN', 'BITF', 'ARBK', 'CORZ', 'CIFR', 'WULF', 'IREN', 'CLSK',
        'COIN', 'SQ', 'PYPL', 'HOOD', 'SI', 'MSTR', 'HUT', 'HIVE'
    ]
    
    # More ETFs - additional leveraged and inverse
    more_etfs = [
        'UPRO', 'SPXU', 'TQQQ', 'SQQQ', 'SOXL', 'SOXS', 'LABU', 'LABD',
        'CURE', 'DRIP', 'FAS', 'FAZ', 'TNA', 'TZA', 'UDOW', 'SDOW',
        'UMDD', 'SMDD', 'URTY', 'SRTY', 'YINN', 'YANG', 'CWEB', 'CHAD',
        'BOIL', 'KOLD', 'GUSH', 'DRIP', 'CORN', 'WEAT', 'UCO', 'SCO',
        'UWT', 'DWT', 'USLV', 'DSLV', 'AGQ', 'ZSL', 'JNUG', 'JDST',
        'NUGT', 'DUST', 'GDXJ', 'GDX', 'SILJ', 'BULZ', 'BERZ'
    ]
    
    # Additional sector and thematic ETFs
    additional_etfs = [
        'SMH', 'SOXX', 'XSD', 'XSW', 'XITK', 'QTEC', 'IGV', 'IGM',
        'IGE', 'IGF', 'SKYY', 'HACK', 'FINX', 'SOCL', 'FDN', 'IBUY',
        'IBB', 'XBI', 'IHI', 'IHF', 'IHE', 'IYT', 'IYZ', 'IYW',
        'IYF', 'IYE', 'IYH', 'IYM', 'IYC', 'IYJ', 'IYR', 'IYW',
        'IYY', 'IYZ', 'IYW', 'IYF', 'IYE', 'IYH', 'IYM', 'IYC',
        'VGT', 'VUG', 'VTV', 'VXF', 'VTHR', 'VONG', 'VONE', 'VTHR',
        'FTEC', 'FCOM', 'FSTA', 'FDIS', 'FENY', 'FMAT', 'FIDU', 'FREL',
        'FINS', 'FITE', 'FXL', 'FXH', 'FXU', 'FXD', 'FXG', 'FXZ'
    ]
    
    # More volatile penny stocks and small caps
    penny_stocks = [
        'SNDL', 'TLRY', 'ACB', 'CGC', 'APHA', 'HEXO', 'OGI', 'CRON',
        'SPCE', 'ASTS', 'OPEN', 'WISH', 'CLOV', 'SPRT', 'SNDL', 'TLRY',
        'NAKD', 'EXPR', 'KOSS', 'BBBY', 'GME', 'AMC', 'BB', 'NOK',
        'F', 'RIDE', 'LCID', 'RIVN', 'NIO', 'XPEV', 'LI', 'RIDE'
    ]
    
    # More growth and momentum stocks
    momentum_stocks = [
        'TSLA', 'NVDA', 'AMD', 'MRNA', 'PLTR', 'RBLX', 'HOOD', 'SOFI',
        'UPST', 'LCID', 'RIVN', 'NIO', 'XPEV', 'LI', 'F', 'RIDE',
        'AFRM', 'COIN', 'SQ', 'PYPL', 'SHOP', 'SNOW', 'DDOG', 'NET',
        'ZS', 'CRWD', 'OKTA', 'DOCN', 'ESTC', 'ASAN', 'ZM', 'PTON',
        'FROG', 'MDB', 'MNDY', 'BILL', 'RPD', 'APP', 'APPN', 'AVPT'
    ]
    
    # More AI and tech stocks
    ai_stocks = [
        'AI', 'BBAI', 'SOUN', 'PLTR', 'C3AI', 'PATH', 'U', 'RPD',
        'NVDA', 'AMD', 'INTC', 'AVGO', 'QCOM', 'TXN', 'MRVL', 'SWKS',
        'MCHP', 'NXPI', 'ON', 'WOLF', 'DIOD', 'ALGM', 'SLAB', 'CRUS',
        'OLED', 'POWI', 'SITM', 'AMBA', 'LSCC', 'MPWR', 'ALGM', 'SLAB'
    ]
    
    # Add hundreds more popular volatile stocks from various sectors
    # Semiconductor stocks
    semis = [
        'NVDA', 'AMD', 'INTC', 'AVGO', 'QCOM', 'TXN', 'MRVL', 'SWKS',
        'MCHP', 'NXPI', 'ON', 'WOLF', 'DIOD', 'ALGM', 'SLAB', 'CRUS',
        'OLED', 'POWI', 'SITM', 'AMBA', 'LSCC', 'MPWR', 'ALGM', 'SLAB',
        'AMAT', 'LRCX', 'KLAC', 'ASML', 'TER', 'ENTG', 'ONTO', 'ACLS'
    ]
    
    # Software/SaaS stocks
    saas_stocks = [
        'SNOW', 'DDOG', 'NET', 'ZS', 'CRWD', 'OKTA', 'DOCN', 'ESTC',
        'ASAN', 'ZM', 'PTON', 'FROG', 'MDB', 'MNDY', 'BILL', 'RPD',
        'APP', 'APPN', 'AVPT', 'BL', 'BSY', 'CFLT', 'FSLY', 'GTLB',
        'NOW', 'PCTY', 'TEAM', 'VEEV', 'WK', 'ZEN', 'ZS', 'CRWD',
        'DOCN', 'ESTC', 'ASAN', 'ZM', 'PTON', 'FROG', 'DDOG', 'NET',
        'AI', 'BBAI', 'SOUN', 'PLTR', 'C3AI', 'PATH', 'U', 'RPD'
    ]
    
    # Fintech stocks
    fintech = [
        'SQ', 'PYPL', 'HOOD', 'SOFI', 'AFRM', 'COIN', 'UPST', 'LCID',
        'RIVN', 'NIO', 'XPEV', 'LI', 'F', 'RIDE', 'SQ', 'PYPL',
        'HOOD', 'SOFI', 'AFRM', 'COIN', 'UPST', 'LCID', 'RIVN', 'NIO'
    ]
    
    # Gaming and entertainment
    gaming = [
        'RBLX', 'EA', 'TTWO', 'ATVI', 'U', 'RPD', 'RBLX', 'EA',
        'TTWO', 'ATVI', 'U', 'RPD', 'RBLX', 'EA', 'TTWO', 'ATVI'
    ]
    
    # Add all major tech companies
    mega_tech = [
        'AAPL', 'MSFT', 'GOOGL', 'GOOG', 'AMZN', 'META', 'NFLX', 'TSLA',
        'NVDA', 'AMD', 'INTC', 'AVGO', 'QCOM', 'TXN', 'MRVL', 'SWKS'
    ]
    
    # Add more biotech and pharma
    more_pharma = [
        'JNJ', 'PFE', 'MRK', 'ABBV', 'TMO', 'DHR', 'A', 'BRKR',
        'WAT', 'PKI', 'ICHR', 'NVCR', 'EXAS', 'NEO', 'GH', 'TDOC',
        'ILMN', 'PACB', 'OMCL', 'TECH', 'TMO', 'DHR', 'A', 'BRKR',
        'ALKS', 'ALNY', 'ARWR', 'BEAM', 'BLUE', 'CRSP', 'EDIT', 'FOLD',
        'IONS', 'NTLA', 'RARE', 'RGNX', 'SGMO', 'ALKS', 'ALNY', 'ARWR'
    ]
    
    # Add many more high-volatility stocks from various categories
    # Energy stocks
    energy_stocks = [
        'XOM', 'CVX', 'COP', 'SLB', 'HAL', 'OXY', 'DVN', 'EOG',
        'MPC', 'VLO', 'PSX', 'HES', 'MRO', 'FANG', 'CTRA', 'OVV',
        'SWN', 'RRC', 'GPOR', 'AR', 'CRK', 'LPI', 'MGY', 'MTDR'
    ]
    
    # Financial stocks
    financial_stocks = [
        'JPM', 'BAC', 'WFC', 'C', 'GS', 'MS', 'SCHW', 'COF',
        'AXP', 'V', 'MA', 'PYPL', 'SQ', 'HOOD', 'SOFI', 'AFRM',
        'COIN', 'SI', 'MSTR', 'RIOT', 'MARA', 'HUT', 'HIVE', 'CAN'
    ]
    
    # Retail and consumer
    retail_stocks = [
        'AMZN', 'WMT', 'TGT', 'HD', 'LOW', 'COST', 'TJX', 'ROST',
        'NKE', 'LULU', 'DKS', 'BBY', 'GME', 'AMC', 'BBBY', 'EXPR'
    ]
    
    # Media and entertainment
    media_stocks = [
        'NFLX', 'DIS', 'PARA', 'WBD', 'FOXA', 'CMCSA', 'RBLX', 'EA',
        'TTWO', 'ATVI', 'U', 'RPD', 'RBLX', 'EA', 'TTWO', 'ATVI'
    ]
    
    # Industrial and materials
    industrial_stocks = [
        'BA', 'CAT', 'GE', 'HON', 'MMM', 'RTX', 'LMT', 'NOC',
        'GD', 'TDG', 'TXT', 'DE', 'CMI', 'PCAR', 'URI', 'FAST'
    ]
    
    # Healthcare services
    healthcare_services = [
        'UNH', 'CVS', 'CI', 'ANTM', 'HUM', 'ELV', 'CNC', 'MOH',
        'TDOC', 'GH', 'NEO', 'EXAS', 'NVCR', 'ICHR', 'PKI', 'WAT'
    ]
    
    # Real estate
    reit_stocks = [
        'AMT', 'PLD', 'EQIX', 'PSA', 'WELL', 'VICI', 'SPG', 'O',
        'DLR', 'EXPI', 'RDFN', 'OPEN', 'Z', 'RDFN', 'EXPI', 'OPEN'
    ]
    
    # Utilities (some can be volatile)
    utility_stocks = [
        'NEE', 'DUK', 'SO', 'AEP', 'SRE', 'EXC', 'XEL', 'WEC',
        'ES', 'ETR', 'PEG', 'ED', 'EIX', 'FE', 'AEE', 'CMS'
    ]
    
    # More small/mid cap tech
    small_tech = [
        'AI', 'BBAI', 'SOUN', 'PLTR', 'C3AI', 'PATH', 'U', 'RPD',
        'APP', 'APPN', 'AVPT', 'BL', 'BSY', 'CFLT', 'FSLY', 'GTLB',
        'NOW', 'PCTY', 'TEAM', 'VEEV', 'WK', 'ZEN', 'ZS', 'CRWD'
    ]
    
    # More biotech small cap
    small_biotech = [
        'ALKS', 'ALNY', 'ARWR', 'BEAM', 'BLUE', 'CRSP', 'EDIT', 'FOLD',
        'IONS', 'NTLA', 'RARE', 'RGNX', 'SGMO', 'ALKS', 'ALNY', 'ARWR',
        'BEAM', 'BLUE', 'CRSP', 'EDIT', 'FOLD', 'IONS', 'NTLA', 'RARE'
    ]
    
    # More crypto and blockchain
    more_blockchain = [
        'COIN', 'SQ', 'PYPL', 'HOOD', 'SI', 'MSTR', 'RIOT', 'MARA',
        'HUT', 'HIVE', 'CAN', 'BITF', 'ARBK', 'CORZ', 'CIFR', 'WULF',
        'IREN', 'CLSK', 'BTBT', 'MSTR', 'HUT', 'HIVE', 'CAN', 'BITF'
    ]
    
    # More EV and auto
    more_ev = [
        'TSLA', 'LCID', 'RIVN', 'NIO', 'XPEV', 'LI', 'F', 'RIDE',
        'GM', 'F', 'STLA', 'HMC', 'TM', 'NIO', 'XPEV', 'LI',
        'LCID', 'RIVN', 'F', 'RIDE', 'TSLA', 'LCID', 'RIVN', 'NIO'
    ]
    
    # More meme and retail favorites
    more_meme = [
        'GME', 'AMC', 'BB', 'NOK', 'SNDL', 'EXPR', 'NAKD', 'KOSS',
        'BBBY', 'CLOV', 'WISH', 'SPRT', 'TLRY', 'ACB', 'CGC', 'APHA',
        'HEXO', 'OGI', 'CRON', 'SNDL', 'ACB', 'CGC', 'TLRY', 'APHA',
        'SPCE', 'ASTS', 'OPEN', 'WISH', 'CLOV', 'SPRT', 'SNDL', 'TLRY'
    ]
    
    # Combine all
    all_etfs = (major_etfs + sector_etfs + leveraged_etfs + bitcoin_etfs + 
                ethereum_related + ark_etfs + thematic_etfs + more_etfs + additional_etfs)
    
    all_stocks = (volatile_tech + meme_stocks + growth_stocks + biotech_volatile + 
                  small_cap_volatile + crypto_mining + ev_stocks + more_volatile +
                  more_tech + more_biotech + more_small_cap + more_crypto +
                  penny_stocks + momentum_stocks + ai_stocks + semis +
                  saas_stocks + fintech + gaming + mega_tech + more_pharma +
                  energy_stocks + financial_stocks + retail_stocks + media_stocks +
                  industrial_stocks + healthcare_services + reit_stocks + utility_stocks +
                  small_tech + small_biotech + more_blockchain + more_ev + more_meme)
    
    # Remove duplicates and return
    unique_etfs = list(set([t.upper() for t in all_etfs if t]))
    unique_stocks = list(set([t.upper() for t in all_stocks if t]))
    
    # Sort for consistency
    unique_etfs.sort()
    unique_stocks.sort()
    
    return {
        'etfs': unique_etfs,
        'stocks': unique_stocks,
        'all': unique_etfs + unique_stocks
    }

