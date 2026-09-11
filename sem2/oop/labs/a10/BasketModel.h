#pragma once
#include <QAbstractTableModel>
#include "TrenchCoat.h"
#include <vector>

class BasketModel : public QAbstractTableModel {
    Q_OBJECT
private:
    std::vector<TrenchCoat> basket;

public:
    explicit BasketModel(QObject* parent = nullptr);

    void setBasket(const std::vector<TrenchCoat>& newBasket);

    int rowCount(const QModelIndex& parent = QModelIndex()) const override;
    int columnCount(const QModelIndex& parent = QModelIndex()) const override;

    QVariant data(const QModelIndex& index, int role = Qt::DisplayRole) const override;
    QVariant headerData(int section, Qt::Orientation orientation, int role = Qt::DisplayRole) const override;
};