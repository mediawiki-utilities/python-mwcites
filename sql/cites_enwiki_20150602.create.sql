CREATE TABLE cites_enwiki_20150602 (
  page_id INT,
  page_title VARBINARY(255),
  rev_id INT,
  timestamp VARBINARY(20),
  type VARCHAR(255),
  id VARCHAR(255)
);
CREATE INDEX type_timestamp ON cites_enwiki_20150602 (type, timestamp);
