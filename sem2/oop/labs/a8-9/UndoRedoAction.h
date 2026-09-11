#pragma once
#include "IRepository.h"
#include "TrenchCoat.h"

// Base abstract class
class UndoRedoAction {
protected:
    IRepository& repo;
public:
    UndoRedoAction(IRepository& repo) : repo(repo) {}
    virtual ~UndoRedoAction() = default;

    virtual void undo() = 0;
    virtual void redo() = 0;
};

// Action for Add operation
class ActionAdd : public UndoRedoAction {
private:
    TrenchCoat addedCoat;
public:
    ActionAdd(IRepository& repo, const TrenchCoat& coat) : UndoRedoAction(repo), addedCoat(coat) {}
    void undo() override { repo.remove_trench_coat(addedCoat); }
    void redo() override { repo.add_trench_coat(addedCoat); }
};

// Action for Remove operation
class ActionRemove : public UndoRedoAction {
private:
    TrenchCoat removedCoat;
public:
    ActionRemove(IRepository& repo, const TrenchCoat& coat) : UndoRedoAction(repo), removedCoat(coat) {}
    void undo() override { repo.add_trench_coat(removedCoat); }
    void redo() override { repo.remove_trench_coat(removedCoat); }
};

// Action for Update operation
class ActionUpdate : public UndoRedoAction {
private:
    TrenchCoat oldCoat;
    TrenchCoat newCoat;
public:
    ActionUpdate(IRepository& repo, const TrenchCoat& oldC, const TrenchCoat& newC)
        : UndoRedoAction(repo), oldCoat(oldC), newCoat(newC) {
    }
    void undo() override { repo.update_trench_coat(newCoat, oldCoat); }
    void redo() override { repo.update_trench_coat(oldCoat, newCoat); }
};
