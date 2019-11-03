CREATE TABLE Congressman
(id INTEGER NOT NULL PRIMARY KEY,
 name VARCHAR(256) NOT NULL,
 house_or_senate CHAR(1) NOT NULL,
 state VARCHAR(2) NOT NULL,
 district INTEGER,
 party CHAR(1) NOT NULL,
 CHECK(house_or_senate in ('rep', 'sen')),
 CHECK(party in ('D', 'R', 'I')),
 CHECK(district IS NOT NULL OR house_or_senate = 'sen'));

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