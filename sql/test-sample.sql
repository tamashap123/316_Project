-- 1. Users register themselves. If logging in with email, they can change personal information. 
INSERT INTO RegisteredUser VALUES('janejohnson@gmail.com', 'Jane Johnson', 'CA', 1);
INSERT INTO RegisteredUser VALUES('xiaomingwang@gmail.com', 'Xiaoming Wang', 'NC', 1);
UPDATE RegisteredUser SET district=3 WHERE email='johndoe@gmail.com';

-- 2. Display all bills with the specified category for the user.
SELECT * FROM Bill WHERE category='Health';

-- 3. Display reprensentatives/senators for the user.
-- NOTE: A senator covers an entire state, regardless of the user's specific district. A house representative covers a sepcific district within a state.
SELECT rep_id FROM RepresentedBy WHERE email='janejohnson@gmail.com';
SELECT rep_id FROM RepresentedBy WHERE email='xiaomingwang@gmail.com';

-- 4. Display congresspersons [along with their sponsorships] that match user searches.
SELECT s.bill_type, s.bill_num, c.name, c.house_or_senate, c.state, c.district, c.party
FROM SponsoredBy s, Congressman c
JOIN Customers ON c.id=s.rep_id and c.id=3;