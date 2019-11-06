-- SQL queries on real sample for milestone .
-- Note: "! Inputs from user" are the user inputs received from the front-end interactions.


-- 1. Users register themselves. If logging in with email, they can change personal information. 
-- ! Inputs from user: email, name, state, district
INSERT INTO RegisteredUser VALUES('janejohnson@gmail.com', 'Jane Johnson', 'CA', 1);
INSERT INTO RegisteredUser VALUES('xiaomingwang@gmail.com', 'Xiaoming Wang', 'NC', 1);
UPDATE RegisteredUser SET district=3 WHERE email='johndoe@gmail.com';

-- 2. Display all bills with the specified category for the user.
-- ! Inputs from user: category
SELECT * FROM Bill WHERE category='Health';

-- 3. Display reprensentatives/senators for the user.
-- NOTE: A senator covers an entire state, regardless of the user's specific district, whereas a house representative only covers a sepcific district within a state.
-- ! Inputs/Implied from user: email
SELECT rep_id FROM RepresentedBy WHERE email='janejohnson@gmail.com';
SELECT rep_id FROM RepresentedBy WHERE email='xiaomingwang@gmail.com';

-- 4.a. Display all sponsorships by searching the exact full name of a reprensentative (using a dropdown menu/autofill).
-- ! Inputs from user: representative name
SELECT b.type, b.num, b.cong_year, b.enacted, b.summary, b.category, b.introduction_date FROM SponsoredBy s, Congressman c, Bill b
WHERE s.rep_id=c.id and s.bill_type = b.type and s.bill_num = b.num and s.cong_year = b.cong_year
and c.name='Kamala D. Harris';

-- 4.b. Display all sponsorships by searching a partial name of a reprensentative (allowing vague search).
-- ! Inputs from user: representative name
INSERT INTO Congressman VALUES('H001099', 'Jane Harris Doe', 'sen', 'CA', NULL, 'Democrat', '202-124-3553', 'Somewhere else', 'https://www.jdharris.senate.gov/contact');
INSERT INTO SponsoredBy VALUES('hr', 2217, 113, 'H001099');

SELECT c.name, b.type, b.num, b.cong_year, b.enacted, b.summary, b.category, b.introduction_date FROM SponsoredBy s, Congressman c, Bill b
WHERE s.rep_id=c.id and s.bill_type = b.type and s.bill_num = b.num and s.cong_year = b.cong_year
and c.name like '%Harris%';

-- 5.a. Display all votes by searching the exact full name of a representative (using a dropdown menu/autofill).
-- ! Inputs from user: representative name
SELECT b.type, b.num, b.cong_year, b.summary, b.category, v.decision FROM Vote v, Congressman c, Bill b
WHERE v.rep_id=c.id and v.bill_type = b.type and v.bill_num = b.num and v.cong_year = b.cong_year
and c.name='G. K. Butterfield';

-- 5.b. Display all votes by searching a partial name of a reprensentative (allowing vague search).
-- ! Inputs from user: representative name
INSERT INTO Congressman VALUES('H021299', 'Butterfield Harris Doe', 'sen', 'CA', NULL, 'Democrat', '202-124-3553', 'Somewhere else', 'https://www.jdharris.senate.gov/contact');
INSERT INTO Vote VALUES('H021299', 'hr', 2217, 113, 'Abstain');

SELECT c.name, b.type, b.num, b.cong_year, b.summary, b.category, v.decision FROM Vote v, Congressman c, Bill b
WHERE v.rep_id=c.id and v.bill_type = b.type and v.bill_num = b.num and v.cong_year = b.cong_year
and c.name like '%Butterfield%';

-- 6. Display all representatives who voted a certain way on a bill, e.g. voted Yea on bill hr2217 in session 113. 
-- ! Inputs from user: bill type, bill num, congress year, vote status
SELECT c.name FROM Vote v, Congressman c
WHERE v.rep_id=c.id and 
v.bill_type='hr' and v.bill_num=2217 and v.cong_year=113 and v.decision='Yea';

-- 7. Display count of votes on bills casted by representatives (house and senate) representing a user.
-- ! Inputs/Implied from user: email

SELECT v.bill_type, v.bill_num, v.cong_year, 
	sum(case when v.decision = 'Yea' then 1 else 0 end) AS YeaCount,
	sum(case when v.decision = 'Nay' then 1 else 0 end) AS NayCount,
	sum(case when v.decision = 'Abstain' then 1 else 0 end) AS AbstainCount
FROM Vote v
WHERE v.rep_id in (SELECT rep_id FROM RepresentedBy WHERE email='xiaomingwang@gmail.com')
GROUP BY v.bill_type, v.bill_num, v.cong_year;

