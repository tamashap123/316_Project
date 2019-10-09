CREATE TABLE Congressman
(id INTEGER NOT NULL PRIMARY KEY,
 name VARCHAR(256) NOT NULL,
 house_or_senate VARCHAR(10) NOT NULL,
 state VARCHAR(2) NOT NULL,
 district INTEGER NOT NULL,
 party VARCHAR(50) NOT NULL);

CREATE TABLE Bill
(type VARCHAR(5) NOT NULL,
 num INTEGER NOT NULL,
 cong_year INTEGER NOT NULL,
 enacted BOOLEAN NOT NULL,
 summary VARCHAR(1000) NOT NULL,
 category VARCHAR(256) NOT NULL,
 introduction_date DATE NOT NULL,
 PRIMARY KEY(type, num));

CREATE TABLE SponsoredBy
(bill_type VARCHAR(5) NOT NULL,
 bill_num INTEGER NOT NULL,
 rep_id INTEGER NOT NULL REFERENCES Congressman(id),
 PRIMARY KEY(bill_type, bill_num, rep_id),
 FOREIGN KEY(bill_type, bill_num) REFERENCES Bill(type, num));

CREATE TABLE Vote
(rep_id INTEGER NOT NULL REFERENCES Congressman(id),
 bill_type VARCHAR(5) NOT NULL,
 bill_num INTEGER NOT NULL,
 decision VARCHAR(10) NOT NULL,
 PRIMARY KEY(rep_id, bill_type, bill_num),
 FOREIGN KEY(bill_type, bill_num) REFERENCES Bill(type, num));

CREATE TABLE RegisteredUser
(email VARCHAR(256) NOT NULL PRIMARY KEY,
 name VARCHAR(256) NOT NULL,
 state VARCHAR(2) NOT NULL,
 district INTEGER NOT NULL);

CREATE TABLE RepresentedBy
(email VARCHAR(256) NOT NULL REFERENCES RegisteredUser(email),
 rep_id INTEGER NOT NULL REFERENCES Congressman(id),
 PRIMARY KEY(email, rep_id));

-- TODO: 
-- - constraints on attributes
-- - trigger on RegisteredUser that updates RepresentedBy?
-- - trigger on Bill that updates SponsoredBy?