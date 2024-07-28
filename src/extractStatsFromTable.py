def getStatsFromTable(tbody):
    rows = tbody.xpath("//tr[*]")
    stats = []
    for row in rows:
        league = row.css("td:nth-child(3) > a:nth-child(1)::text").extract()
        if not league or not league[0].strip() == "GRE-1":
            continue

        cols = []
        for col in row.css("td *::text"):
            processed_col = col.extract().strip()
            if processed_col:
                cols.append(processed_col)

        if len(cols[0]) > 5:
            continue

        stats.append(cols)
        
    return stats

def createStatEntry(stats): 
    statEntry = {}
    for row in stats:
        season = 2000 + int(row[0].split("-")[0])
        team = row[1]
        statEntry[season] = {"Team" : team,
                             "Stats" : row[3:]}
    return statEntry