#include "BasketModel.h"

BasketModel::BasketModel(QObject* parent)
    : QAbstractTableModel(parent)
{
}

void BasketModel::setBasket(const std::vector<TrenchCoat>& newBasket)
{
    beginResetModel();
    this->basket = newBasket;
    endResetModel();
}

int BasketModel::rowCount(const QModelIndex& parent) const
{
    if (parent.isValid())
        return 0;
    return static_cast<int>(this->basket.size());
}

int BasketModel::columnCount(const QModelIndex& parent) const
{
    if (parent.isValid())
        return 0;
    return 3; // columns: size, colour, price
}

QVariant BasketModel::data(const QModelIndex& index, int role) const
{
    if (!index.isValid() || role != Qt::DisplayRole)
        return QVariant();

    const auto& coat = this->basket[index.row()];
    switch (index.column()) {
    case 0:
        return QString::fromStdString(coat.get_size());
    case 1:
        return QString::fromStdString(coat.get_colour());
    case 2:
        return QString("$%1").arg(coat.get_price());
    default:
        return QVariant();
    }
}

QVariant BasketModel::headerData(int section, Qt::Orientation orientation, int role) const
{
    if (role != Qt::DisplayRole)
        return QVariant();

    if (orientation == Qt::Horizontal) {
        switch (section) {
        case 0: return QString("Size");
        case 1: return QString("Colour");
        case 2: return QString("Price");
        default: return QVariant();
        }
    }
    return QVariant();
}