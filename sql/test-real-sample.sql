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
INSERT INTO Congressman VALUES('H001099', 'Jane Harris Doe', 'sen', 'CA', NULL, 'Democrat', '202-124-3553', 'Somewhere else', 'https://www.jdharris.senate.gov/contact');
INSERT INTO SponsoredBy VALUES('hr', 2217, 113, 'H001099');

SELECT c.name, b.type, b.num, b.cong_year, b.enacted, b.summary, b.category, b.introduction_date FROM SponsoredBy s, Congressman c, Bill b
WHERE s.rep_id=c.id and s.bill_type = b.type and s.bill_num = b.num and s.cong_year = b.cong_year
and c.name like '%Harris%';
