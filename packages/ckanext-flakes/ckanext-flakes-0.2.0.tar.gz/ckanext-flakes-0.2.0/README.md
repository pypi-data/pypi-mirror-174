[![Tests](https://github.com/DataShades/ckanext-flakes/workflows/Tests/badge.svg?branch=main)](https://github.com/DataShades/ckanext-flakes/actions)

# ckanext-flakes

Tools for creating and managing independent chunks of data.

This extension provides a base entity for storing arbitrary data. It can be
used in a number of cases, especially, if you don't want yet to create a brand
new model, database migrations and tables, but you have no other options.

`ckanext-flakes` gives you a set of actions for creating and managing small
dictionary-like objects(anything, that can be serialized into JSON). If you are
using it and want to add an extra action, feel free to create a PR or an issue
with your suggestion.

## Structure

* [Examples](#examples)
* [Definition](#definition)
* [Requirements](#definition)
* [Installation](#installation)
* [Configuration](#configuration)
* [Interfaces](#interfaces)
* [API](#api)
  * [`flakes_flake_create`](#flakes_flake_create)
  * [`flakes_flake_show`](#flakes_flake_show)
  * [`flakes_flake_list`](#flakes_flake_list)
  * [`flakes_flake_update`](#flakes_flake_update)
  * [`flakes_flake_override`](#flakes_flake_override)
  * [`flakes_flake_delete`](#flakes_flake_delete)
  * [`flakes_flake_lookup`](#flakes_flake_lookup)
  * [`flakes_flake_validate`](#flakes_flake_validate)
  * [`flakes_data_validate`](#flakes_data_validate)
  * [`flakes_data_example`](#flakes_data_example)
  * [`flakes_flake_materialize`](#flakes_flake_materialize)
  * [`flakes_flake_combine`](#flakes_flake_combine)
  * [`flakes_flake_merge`](#flakes_flake_merge)
  * [`flakes_data_patch`](#flakes_data_patch)
  * [`flakes_extras_patch`](#flakes_extras_patch)

## Examples

TODO list operations via flakes.

First, let's create two task.

```bash

ckanapi action flakes_create_flake \
    data='{"task": "add examples", "done": false}' \
    extras='{"topic": "todo"}'


ckanapi action flakes_create_flake \
    name=todo/rest
    data='{"task": "rest a bit", "done": false}' \
    extras='{"topic": "todo"}'

```

### Definition

Whenever you see the word **flake** below, it means a record, that contains
an arbitrary dictionary. A couple of facts:

* *flakes* can be obtained only by their author. It means, you can store
  private data there.
* Absolutely every *flake* contains data. At least an empty dictionary. But there
  is no flake that has no data at all.
* *Flake* can hold extra details, that are not a part of the data. Its purpose,
  description, tags, anything(just like `plugin_extras` inside the User
  model). Extra details are just a separate dictionary that can hold any
  information that is important for the *flake* but cannot be placed inside the
  *flake*'s primary data.
* *Flakes* belong to the user. There is no unowned *flake*. Whenever owner is
  removed, all his flakes removed as well.
* *Flake* can have a name. Not necessary, but if you want to create a very
  special *flake*, you can give it a name. You cannot have two *flakes* with
  the same name(because every named flake is **really special** for you). But
  other users can use the same names for their flakes as you do. In other
  words, *flake*'s **name** is unique per user.
* *Flake* can have a **parent**. If the parent is removed, all its descendants
  removed as well. **Parent** extends *flake*'s data, providing default
  values. The behavior of the *flake* with a **parent** is very similar to the
  built-in `collections.ChainMap`. *Flake* can have only one parent, so there
  are no things like python's method resolution order.
* [*Flake* can be validated](#flakes_flake_validate).
* *Flakes* can be combined. Check
  [`flakes_flake_combine`](#flakes_flake_combine) and
  [`flakes_flake_merge`](#flakes_flake_merge) actions below.

### Where you can use it?

* You want to create a **TODO list inside your application**. You actually can
  * define custom dataset type for this purpose
  * Create migration, model, set of actions

  Easy, but I've done it too many times and at some point, I even created
  macros for such tasks. Do I have to do it again? Hmmm.. why not use *flakes*?
  They can hold arbitrary data, such as task, deadline, and state. By default,
  *flakes* are visible only to the owner(and sysadmin, of course), so they
  won't leak to other users. And you can use *flake*'s extra in order to set,
  for example, the task's subject and use it for filtering via
  [`flakes_flake_list`](#flakes_flake_list). The only thing you need to do
  is a UI for the TODO list. But you have to do it anyway because it must be
  styled using your app's style guidelines and branding colors.

* You need to create **resources before the dataset**. Don't know why, but you
  have all the resource details(except for the uploaded file because *flakes*
  are about information, not about files). CKAN will not be happy if you try
  `resource_create` without the dataset's ID.

  But how about creating a *flake*? Put all the details into it and forget
  about the resource. Take a break or even vacation. Get back to work, and
  create a dataset. Add dataset's ID to the existing flake via
  [`flakes_flake_update`](#flakes_flake_update) or
  [`flakes_flake_override`](#flakes_flake_override). And turn it into a
  resource using [`flakes_flake_materialize`](#flakes_flake_materialize).

* You are developing **multi-step dataset creation form**. Sounds cool. But you
  have to store different pieces of dataset somewhere. Of course, if you don't
  have an overprotective validation schema, you can just save all the parts
  inside the draft dataset. But if you do have such schema.. well, you know
  what I'll recommend, right? Just create a bunch of *flakes*, [combine them
  into a dictionary](#flakes_flake_combine), and send this dictionary to
  the `package_create`. Or [merge them into a new
  flake](#flakes_flake_merge) and [materialize using API action on your
  choice](#flakes_flake_materialize). Have you said
  ["validation"](#flakes_data_validate)? Or you meant [another
  "validation"](#flakes_flake_validate)?

* How about a **user-request functionality**? User has a `state` so you can
  create a *pending* user account, that requires approval. But when somebody
  creates a user request, he can give you extra details, like the reason to join
  the portal, the organization in which the new user wants to be a member, etc. You
  already know what to do.

* Actually, **anything that requires some sort of approval** can use
  *flakes*:

  * Dataset suggestion? Yes, you don't need a draft dataset here.
  * Dataset revision, that must be approved, before an actual dataset is
    updated? Why not? If you prefer to clone the dataset, modify the clone, and
    merge it back, it's ok. But if it's overkill for your case and you just
    need small patches, *flake* may save you a day or two.
  * Request to move a dataset from one organization to another or mark it as
    obsolete/superseeded? I don't mind.

---

## Requirements

Requires python v3.7 or greater. Python v2 support doesn't require much effort,
but it neither worth the time you'll spend on it.


Compatibility with core CKAN versions:

| CKAN version | Compatible? |
|--------------|-------------|
| 2.9          | yes         |
| 2.10         | yes         |


## Installation

To install ckanext-flakes:

1. Install it via **pip**:

        pip install ckanext-flakes

1. Add `flakes` to the `ckan.plugins` setting in your CKAN config file.
1. Run DB migrations:

        ckan db upgrade -p flakes

## Configuration

	# Allow logged-in user to create flakes.
    # When disabled, only sysadmin can work with flakes.
	# (optional, default: true).
    ckanext.flakes.creation.allowed = no

	# Allow validation. Depending on your validation schemas,
    # it can potentially discover some sensitive information.
	# For example, there is a validator, which verifies that user ID exists.
    # That's why validation is disabled by default.
	# (optional, default: false).
    ckanext.flakes.validation.allowed = yes

## Interfaces

Provides `ckanext.flakes.interfaces.IFlakes` interface. Always use
`inherit=True` when implementing it, because it may change in the future.

Currently it provides the following hooks:

```python
class IFlakes(Interface):
    """Extend functionality of ckanext-flakes"""

    def get_flake_schemas(self) -> dict[str, dict[str, Any]]:
        """Register named validation schemas.

        Used by `flakes_flake_validate` and `flakes_data_validate` actions.

        Returns:
            Mapping of names and corresponding validation schemas.

        Example:
            def get_flake_schemas(self) -> dict[str, dict[str, Any]]:
                return {
                    "schema-that-requires-name": {"name": [not_missing]}
                }
        """
        return {}

    def get_flake_factories(self) -> dict[str, Callable[[dict[str, Any]], dict[str, Any]]]:
        """Register named example factories.

        Used by `flakes_data_example` action.

        Returns:
            Mapping of names and corresponding example factories.

        Example:
            def get_flake_factories(self) -> dict[str, dict[str, Any]]:
                def factory(payload: dict[str, Any]):
                    return {"field": "value"}

                return {
                    "test-factory": factory
                }
        """
        return {}
```


## API

### `flakes_flake_create`

Create a flake.

Args:

    name (str, optional): name of the flake
    data (dict): flake's data
    parent_id (str, optional): ID of flake to extend
    extras (dict): flake's extra details

### `flakes_flake_show`

Display existing flake

Args:

    id (str): ID of flake to display
    expand (bool, optional): Extend flake using data from the parent flakes


### `flakes_flake_list`

Display all flakes of the user.

If `extras` dictionary passed, show only flakes that contains given extras. Example:

    first_flake = Flake(extras={"xxx": {"yyy": "hello"}})
    second_flake = Flake(extras={"xxx": {"yyy": "world"}})

    flake_list(context, {"extras": {"xxx": {"yyy": "hello"}})
    >>> first_flake

Args:

    expand (bool, optional): Extend flake using data from the parent flakes
    extras (dict, optional): Show only flakes whose extras contains passed dict


### `flakes_flake_update`

Update existing flake

Args:

    id (str): ID of flake to update
    data (dict): flake's data
    parent_id (str, optional): ID of flake to extend
    extras (dict): flake's extra details

### `flakes_flake_override`

Update existing flake by name or create a new one.

Args:

    name (str): Name flake to override
    data (dict): template itself
    parent_id (str, optional): ID of flake to extend
    extras (dict): flake's extra details

### `flakes_flake_delete`

Delete existing flake

Args:

    id (str): ID of flake to delete

### `flakes_flake_lookup`

Display flake using its name.

Args:

    name (str): Name of the flake

### `flakes_flake_validate`

Validate existing flake

Schemas must be registered via `IFlakes` interface.

Args:

    id (str): ID of flake to validate
    expand (bool, optional): Extend flake using data from the parent flakes
    schema(str): validation schema for the flake's data


### `flakes_data_validate`

Validate arbitrary data against the named schema(registered via IFlakes).

Args:

    data (dict): data that needs to be validated
    schema(str): validation schema for the data

### `flakes_data_example`

Generate an example of the flake's data using named factory(registered via IFlakes).

Factories must be registered via `IFlakes` interface.

Args:

    factory(str): example factory
    data (dict, optional): payload for the example factory

### `flakes_flake_materialize`

Send flake's data to API action.

Args:

    id (str): ID of flake to materialize
    expand (bool, optional): Extend flake using data from the parent flakes
    remove (bool, optional): Remove flake after materialization
    action (str): API action to use for materialization

### `flakes_flake_combine`

Combine data from multiple flakes

`id` argument specifies all the flakes that must be combined. All of the flakes
must exist, otherwise `NotFound` error raised. IDs at the start of the list have
higher priority(override matching keys). IDs at the end of the list have lower
priority(can be shadowed by former flakes).

`expand` must be a `dict[str, bool]`. Keys are IDs of the flakes, values are
expand flags for the corresponding flake.

Args:

    id (list): IDs of flakes.
    expand (dict, optional): Extend flake using data from the parent flakes

### `flakes_flake_merge`

Combine multiple flakes and save the result.

Args:

    id (list): IDs of flakes.
    expand (dict, optional): Extend flake using data from the parent flakes
    remove (bool, optional): Remove flakes after the operation.
    destination (str, optional): Save data into the specified flake instead of a new one

### `flakes_data_patch`

Partially overrides data leaving other fields intact.

Args:

    id (str): ID of flake
    data (dict): patch for data


### `flakes_extras_patch`

Partially overrides extras leaving other fields intact.

Args:

    id (str): ID of flake
    extras (dict): patch for extras

## Developer installation

To install ckanext-flakes for development, activate your CKAN virtualenv and
do:

    git clone https://github.com/DataShades/ckanext-flakes.git
    cd ckanext-flakes
    python setup.py develop


## Tests

To run the tests, do:

    pytest

## License

[AGPL](https://www.gnu.org/licenses/agpl-3.0.en.html)
