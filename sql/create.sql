CREATE TABLE Congressman
(id VARCHAR(15) NOT NULL PRIMARY KEY,
 name VARCHAR(256) NOT NULL,
 house_or_senate VARCHAR(5) NOT NULL,
 state VARCHAR(2) NOT NULL,
 district INTEGER,
 party VARCHAR(15) NOT NULL,
 phone VARCHAR(15) NOT NULL,
 address VARCHAR(256) NOT NULL,
 contact_form VARCHAR(256),
 CHECK(house_or_senate in ('rep', 'sen')),
 CHECK(party in ('Democrat', 'Republican', 'Independent')),
 CHECK(district IS NOT NULL OR house_or_senate = 'sen'));

CREATE TABLE Bill
(type VARCHAR(2) NOT NULL,
 num INTEGER NOT NULL,
 cong_year INTEGER NOT NULL,
 enacted BOOLEAN NOT NULL,
 summary VARCHAR(10000) NOT NULL,
 category VARCHAR(256) NOT NULL,
 introduction_date DATE NOT NULL,
 PRIMARY KEY(type, num, cong_year),
 CHECK(type in ('hr','s')),
 CHECK(cong_year <= 116));

CREATE TABLE SponsoredBy
(bill_type VARCHAR(2) NOT NULL,
 bill_num INTEGER NOT NULL,
 cong_year INTEGER NOT NULL,
 rep_id VARCHAR(15) NOT NULL REFERENCES Congressman(id),
 PRIMARY KEY(bill_type, bill_num, cong_year, rep_id),
 FOREIGN KEY(bill_type, bill_num, cong_year) REFERENCES Bill(type, num, cong_year));

CREATE TABLE Vote
(rep_id VARCHAR(15) NOT NULL REFERENCES Congressman(id),
 bill_type VARCHAR(2) NOT NULL,
 bill_num INTEGER NOT NULL,
 cong_year INTEGER NOT NULL,
 decision VARCHAR(10) NOT NULL,
 PRIMARY KEY(rep_id, bill_type, bill_num, cong_year),
 FOREIGN KEY(bill_type, bill_num, cong_year) REFERENCES Bill(type, num, cong_year),
 CHECK(decision in ('Aye', 'Nay', 'Abstain')));

CREATE TABLE RegisteredUser
(email VARCHAR(256) NOT NULL PRIMARY KEY,
 name VARCHAR(256) NOT NULL,
 state VARCHAR(2) NOT NULL,
 district INTEGER NOT NULL);

CREATE TABLE RepresentedBy
(email VARCHAR(256) NOT NULL REFERENCES RegisteredUser(email),
 rep_id VARCHAR(15) NOT NULL REFERENCES Congressman(id),
 PRIMARY KEY(email, rep_id));

CREATE FUNCTION F_Get_Representatives() RETURNS TRIGGER AS $$
BEGIN
	INSERT INTO RepresentedBy(email, rep_id) (
		SELECT NEW.email, Congressman.id
		FROM Congressman
		WHERE (Congressman.house_or_senate = 'sen' AND Congressman.state = NEW.state) 
			OR (Congressman.house_or_senate = 'rep' AND Congressman.state = NEW.state AND Congressman.district = NEW.district)
	);
	RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER T_Get_Representatives
 AFTER INSERT ON RegisteredUser
 FOR EACH ROW
 EXECUTE PROCEDURE F_Get_Representatives();

CREATE FUNCTION F_Update_Representatives() RETURNS TRIGGER AS $$
BEGIN
	DELETE FROM RepresentedBy
	WHERE email = OLD.email;
	IF (TG_OP = 'UPDATE') THEN
		INSERT INTO RepresentedBy(email, rep_id) (
			SELECT NEW.email, Congressman.id
			FROM Congressman
			WHERE (Congressman.house_or_senate = 'sen' AND Congressman.state = NEW.state) 
				OR (Congressman.house_or_senate = 'rep' AND Congressman.state = NEW.state AND Congressman.district = NEW.district)
		);
		RETURN NEW;
	END IF;
	RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER T_Update_Representatives
 BEFORE UPDATE OR DELETE ON RegisteredUser
 FOR EACH ROW
 EXECUTE PROCEDURE F_Update_Representatives();