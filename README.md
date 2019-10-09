<h1 align="center">CompSci 316 Course Project</h1>
<h4 align="center">Anna Cunningham, Jonathon Kuo, Janice Liu, Tamasha Pathirathna, Vicki Zhang</h4>
<h4 align="center">Fall 2019</h4>
<hr>
<h3>Instructions to Create and Load Sample Database</h3>
<p>Within the course VM, navigate to the <code>sql</code> directory. Then, issue the following commands to (re)create the database named <code>congress</code> and populate it with small sample data:<br>
<code>dropdb congress; createdb congress; psql congress -af create.sql; psql congress -af load-sample.sql</code>
</p>