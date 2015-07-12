SELECT
  LEFT(timestamp, 7) AS month,
  type,
  COUNT(*) AS citations
FROM cites_enwiki_20150602
GROUP BY 1,2;
