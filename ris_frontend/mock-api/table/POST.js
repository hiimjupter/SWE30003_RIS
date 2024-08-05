module.exports = (req, res) => {
    const tableId = req.body.id;

    if (tableId === 1) {
        return res.sendStatus(409);
    }   
    
    return res.status(201).send({
        "id": req.body.id,
        "table": req.body.table
    });
}