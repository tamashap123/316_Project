-- SQL queries on toy sample for milestone 2.
-- 1. Users register themselves. If logging in with email, they can change personal information. 
INSERT INTO RegisteredUser VALUES('janejohnson@gmail.com', 'Jane Johnson', 'CA', 1);
INSERT INTO RegisteredUser VALUES('xiaomingwang@gmail.com', 'Xiaoming Wang', 'NC', 1);
UPDATE RegisteredUser SET district=3 WHERE email='johndoe@gmail.com';

-- 2. Display all bills with the specified category for the user.
SELECT * FROM Bill WHERE category='Health';

-- 3. Display reprensentatives/senators for the user.
-- NOTE: A senator covers an entire state, regardless of the user's specific district, whereas a house representative only covers a sepcific district within a state.
SELECT rep_id FROM RepresentedBy WHERE email='janejohnson@gmail.com';
SELECT rep_id FROM RepresentedBy WHERE email='xiaomingwang@gmail.com';

-- 4. Display all sponsorships by a reprensentative.
SELECT s.bill_type, s.bill_num FROM SponsoredBy s, Congressman c
WHERE s.rep_id=c.id and c.name='Kamala Harris';

-- 5. Display all votes by a representative.
SELECT v.bill_type, v.bill_num, v.decision FROM Vote v, Congressman c
WHERE v.rep_id=c.id and c.name='George Butterfield Jr.';

-- 6. Display all representatives who voted a certain way on a bill, e.g. voted Aye on bill H-2217. 
SELECT c.name FROM Vote v, Congressman c
WHERE v.rep_id=c.id and v.bill_type='H' and v.bill_num=2217 and v.decision='Aye';

-- 7. Display all votes on bills casted by representatives (house and senate) representing a user.
SELECT * FROM Vote v
WHERE v.rep_id in (SELECT rep_id FROM RepresentedBy WHERE email='xiaomingwang@gmail.com')
GROUP BY v.bill_type, v.bill_num, v.rep_id;

-- 8. Tally the numbers of Ayes and Nays on a bill.
SELECT sum(case when v.decision = 'Aye' then 1 else 0 end) AS Aye_Count, 
sum(case when v.decision = 'Nay' then 1 else 0 end) AS Nay_Count FROM Vote v
WHERE v.bill_type='H' and v.bill_num=2217;

-- 9. Compare two representatives' votes.
SELECT A.bill_type, A.bill_num, A.rep_id as Rep1, A.decision as Rep1_Decision, B.rep_id as Rep2, B.decision as Rep2_Decision 
FROM ((SELECT * FROM Vote as v1 WHERE v1.rep_id=2) A JOIN (SELECT * FROM Vote as v2 WHERE v2.rep_id=3) B
	ON A.bill_type=B.bill_type and A.bill_num=B.bill_num);

-- 10. Display bills that are introduced after a certain date.
SELECT * FROM Bill
WHERE introduction_date>DATE(CAST('2010-03-23' AS VARCHAR));

