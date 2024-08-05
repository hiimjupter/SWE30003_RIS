module.exports = (req, res) => {
    const tableId = req.body.table_id;

    if (tableId === 1) {
        return res.sendStatus(409);
    }   
    
    return res.status(201).send({
        "id": req.body.table_id,
        "table": req.body.table
    });
};