module.exports = (req, res) =>
  res.status(200).json({
    id: 0,
    userName: req.params.table,
    age: 20
  });