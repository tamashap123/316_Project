CREATE TABLE Congressman
(id INTEGER NOT NULL PRIMARY KEY,
 name VARCHAR(256) NOT NULL,
 house_or_senate CHAR(1) NOT NULL,
 state VARCHAR(2) NOT NULL,
 district INTEGER,
 party CHAR(1) NOT NULL,
 CHECK(house_or_senate in ('H', 'S')),
 CHECK(party in ('D', 'R', 'I')),
 CHECK(district IS NOT NULL OR house_or_senate = 'S'));

CREATE TABLE Bill
(type CHAR(1) NOT NULL,
 num INTEGER NOT NULL,
 cong_year INTEGER NOT NULL,
 enacted BOOLEAN NOT NULL,
 summary VARCHAR(1000) NOT NULL,
 category VARCHAR(256) NOT NULL,
 introduction_date DATE NOT NULL,
 PRIMARY KEY(type, num),
 CHECK(type in ('H','S')),
 CHECK(cong_year < 116));

CREATE TABLE SponsoredBy
(bill_type CHAR(1) NOT NULL,
 bill_num INTEGER NOT NULL,
 rep_id INTEGER NOT NULL REFERENCES Congressman(id),
 PRIMARY KEY(bill_type, bill_num, rep_id),
 FOREIGN KEY(bill_type, bill_num) REFERENCES Bill(type, num));

CREATE TABLE Vote
(rep_id INTEGER NOT NULL REFERENCES Congressman(id),
 bill_type CHAR(1) NOT NULL,
 bill_num INTEGER NOT NULL,
 decision VARCHAR(10) NOT NULL,
 PRIMARY KEY(rep_id, bill_type, bill_num),
 FOREIGN KEY(bill_type, bill_num) REFERENCES Bill(type, num),
 CHECK(decision in ('Aye', 'Nay', 'Abstain')));

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
-- - trigger on RegisteredUser that updates RepresentedBy?

CREATE FUNCTION F_Get_Representatives() RETURNS TRIGGER AS $$
BEGIN
 IF (TG_OP = 'INSERT') THEN
 	-- INSERT INTO RepresentedBy (
 	-- 	SELECT RegisteredUser.email, Congressman.id
 	-- 	FROM Congressman, RegisteredUser
 	-- 	WHERE RegisteredUser.email = NEW.email 
 	-- 	AND ((Congressman.house_or_senate = 'S' AND Congressman.state = RegisteredUser.state) 
 	-- 		OR (Congressman.house_or_senate = 'H' AND Congressman.state = RegisteredUser.state AND Congressman.district = RegisteredUser.district))
 	-- );
 END IF;
 IF (TG_OP = 'UPDATE') THEN

 END IF;
 RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER T_Get_Representatives
 AFTER INSERT OR UPDATE ON RegisteredUser
 EXECUTE PROCEDURE F_Get_Representatives();