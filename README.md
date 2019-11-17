<h1 align="center">CompSci 316 Course Project</h1>
<h4 align="center">Anna Cunningham, Jonathon Kuo, Janice Liu, Tamasha Pathirathna, Vicki Zhang</h4>
<h4 align="center">Fall 2019</h4>
<hr>
<h3>Instructions to Create and Load Sample Database</h3>
<p>Within the course VM, navigate to the <code>sql</code> directory. Then, issue the following commands to (re)create the database named <code>congress</code> and populate it with small sample data:<br>
<code>dropdb congress; createdb congress; psql congress -af create.sql; psql congress -af load-sample.sql</code>
</p>
<h3>Instructions to Create and Load Production Database</h3>
<p>Within the course VM, navigate to the <code>sql</code> directory. Then, issue the following commands to (re)create the database named <code>congress</code> and populate it with the real data:<br>
<code>dropdb congress; createdb congress; psql congress -qf create.sql; psql congress -qf load-production-congresspeople.sql; psql congress -qf load-production-bills.sql; psql congress -qf load-production-votes.sql</code>
<br>
Note that some of the <code>INSERT</code> statements will result in errors since there were some discrepancies between congressmen data and voting data (due to more recent resignations, deaths, etc.). 
</p>