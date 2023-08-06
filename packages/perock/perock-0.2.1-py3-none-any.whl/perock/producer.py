'''
Defines producer classes to be used by 'bforce' module.

Author: Sekgobela Kevin
Date: June 2022
Languages: Python 3
'''
from typing import Callable, Iterable, Iterator
import itertools

from . import forcetable


class ProducerBase():
    '''Base producer class for produsing items'''
    def __init__(self, items_source) -> None:
        self._items_source = items_source
        self._fetched_items = self.fetch_items()
        self._producer_should_cancel = False

        self._external_cancel_callback = lambda item: None
        self._external_item_return_callback = lambda item: None
        self._external_item_return_fail_callback = lambda item: None

    def set_cancel_callback(self, callback: Callable):
        self._external_cancel_callback = callback

    def set_item_return_callback(self, callback: Callable):
        self._external_item_return_callback = callback

    def set_return_fail_callback(self, callback: Callable):
        self._external_item_return_fail_callback = callback


    def set_cancel_callable(self, callable_):
        self._external_cancel_callable = callable_

    def set_item_return_callable(self, callable_):
        self._external_item_return_callable = callable_

    def fetch_items(self) -> Iterable:
        # Fetches items from items_source
        raise NotImplementedError("fetch_items(self) not implemented")

    def should_return_item(self, item) -> bool:
        #raise NotImplementedError("should_return_item() not implemented")
        return True

    def filter_items(self, fetched_items):
        return fetched_items

    def get_items(self) -> Iterator:
        # Filtering is performed while getting items.
        return self.filter_items(self._fetched_items)

    def _item_return_fail_callback(self, item):
        # Called when item couldnt be returned by producer
        self._external_item_return_fail_callback(item)

    def _item_return_callback(self, item):
        # Called when item is returned by producer
        self._external_item_return_callback(item)

    def _cancel_callback(self):
        self._external_cancel_callback()

    def cancel(self):
        self._producer_should_cancel = True

    def __iter__(self):
        return self.get_items()



class RecordsProducer(ProducerBase):
    '''Base producer class for records'''
    def __init__(self, table: forcetable.Table) -> None:
        self._table = table
        self._items_source: forcetable.Table
        self._fetched_items: Iterable[forcetable.Record]
        super().__init__(table)

        self._fetched_records = self._fetched_items

    def fetch_items(self) -> Iterable[forcetable.Record]:
        return iter(self._table)

    def filter_items(self, fetched_items):
        # Filters fetched items while calling callback functions.
        for item in fetched_items:
            if self._producer_should_cancel:
                self._cancel_callback(item)
                break
            elif self.should_return_item(item):
                self._item_return_callback(item)
                yield item
            else:
                self._item_return_fail_callback(item)
                pass


class LoopAllProducer(RecordsProducer):
    '''Producer for records that loops and check each record'''
    def __init__(self, table: forcetable.Table) -> None:
        super().__init__(table)


class LoopSomeProducer(RecordsProducer):
    '''Producer for records that loops and check olny neccessay records'''
    def __init__(self, table: forcetable.Table) -> None:
        super().__init__(table)
        self._excluded_primary_items = set()
        self._fields = self._table.get_fields()
        self._primary_field_exists = self._table.primary_field_exists()

        # Allows multiple primary items to be tried
        self._max_multiple_primary_items = 1
        # Maximum success records for primary item before swicthing.
        self._max_primary_item_records = 1

        self._primary_grouped_records = iter(
            self._table.records_primary_grouped()
        )
        self._current_primary_grouped_records = set()
        self._current_primary_grouped_records_cycle = itertools.cycle(
            self._current_primary_grouped_records
        )

        # External callback functions
        self._producer_switch_callback = None

        # Callable to decide if producer should switch.
        self._producer_switch_records_callable = None

    def set_producer_switch_callback(self, callback):
        # Sets callback when producer switches
        self._producer_switch_callback = callback


    def set_max_multiple_primary_items(self, total):
        self._max_multiple_primary_items = total

    def set_max_primary_item_records(self, total):
        self._max_primary_item_records = total


    def set_producer_switch_records_callable(self, callable_):
        self._should_switch_records_callable = callable_


    def add_excluded_primary_item(self, primary_item):
        self._excluded_primary_items.add(primary_item)

    def add_excluded_primary_items(self, primary_items):
        for item in primary_items:
            self.add_excluded_primary_item(item)

    def remove_excluded_primary_item(self, primary_items):
        for item in primary_items:
            self.add_excluded_primary_item(item)

    def remove_excluded_primary_items(self, primary_item):
        self.remove_excluded_primary_item(primary_item)

    def update_current_records(self):
        # Holds maximum parallel primary tasks
        max_parallel_tasks = self._max_multiple_primary_items
        # Holds current primary grouped records
        primary_grouped_records = self._current_primary_grouped_records
        while len(primary_grouped_records) < max_parallel_tasks:
            try:
                # Get records and wrap them in iterator
                records = iter(next(self._primary_grouped_records))
            except StopIteration:
                # Breaks as we ran out of records
                break
            else:
                # Add record to current primary grouped records
                self._current_primary_grouped_records.add(records)

    def _update_current_records_cycle(self):
        # Firstly update current records
        self.update_current_records()
        # Update itertools cycle object with records
        self._current_primary_grouped_records_cycle = itertools.cycle(
            self._current_primary_grouped_records
        )

    def remove_from_current_records(self, records_iter):
        # Remove records from current grouped records and update
        # cycle
        self._current_primary_grouped_records.discard(records_iter)
        self._update_current_records_cycle()

    def add_to_current_records(self, records_iter):
        # Add records to current grouped records and update
        # cycle
        self._current_primary_grouped_records.add(records_iter)
        self._update_current_records_cycle()

    def current_records_empty(self):
        # Checks if current records are empty
        return len(self._current_primary_grouped_records) == 0

    def get_next_records(self):
        # Gets next current records from current grouped records cycle
        try:
            # Attempts to get current records
            return next(self._current_primary_grouped_records_cycle)
        except StopIteration:
            # load new records if records were not found
            self._update_current_records_cycle()
            if self.current_records_empty():
                # Return as there are no records left
                return None
            else:
                # Try again to get next records
                return self.get_next_records()


    def get_next_record_records(self):
        # Gets nex record with other records
        records = self.get_next_records()
        if records == None:
            return (None, None)
        try:
            # Return record from records
            record = next(records)
        except StopIteration:
            # Remove the records it has been exausted the end
            self.remove_from_current_records(records)
            # Try again to get record
            return self.get_next_record_records()
        else:
            return (record, records)

    
    def _get_next_record(self):
        # Gets next record, None if no record
        return self.get_next_record_records()[0]

    def fetch_items(self) -> Iterable[forcetable.Record]:
        if self._table.primary_field_exists():
            while True:
                record, records = self.get_next_record_records()
                if record != None:
                    if self.should_switch_to_next_records(record):
                        # Remove records from current primary records
                        self.remove_from_current_records(records)
                        self.switch_to_next_records_callback(record)
                    yield record
                else:
                    # Ran out of records
                    self.switch_to_next_records_callback(record)
                    break
        else:
            err_msg = "Current producer requires primary field"
            raise Exception(err_msg)

    def should_return_item(self, record) -> bool:
        #raise NotImplementedError("should_return_item() not implemented")
        primary_field = self._table.get_primary_field()
        primary_field_name = primary_field.get_item_name()
        record_primary_item = record[primary_field_name]
        # Only return record if its primary item not in excluded
        # primary item
        return record_primary_item not in self._excluded_primary_items

    def should_switch_to_next_records(self, record=None):
        # Returns True if producer should swicth to next primary records
        if record is None:
            return False
        elif self._producer_switch_records_callable:
            return self._producer_switch_records_callable(record)
        else:
            return not self.should_return_item(record)

    def switch_to_next_records_callback(self, record):
        # Called when primary record are swiched.
        # Record is last record before swicth or None.
        if self._producer_switch_callback:
            self._producer_switch_callback(record)
    



if __name__ == "__main__":

    usernames = range(14)
    passwords = range(1000)

    # Creates fields for table
    usernames_col = forcetable.Field('usernames', usernames)
    # Sets key name to use in record key in Table
    usernames_col.set_item_name("username")
    passwords_col = forcetable.Field('passwords', passwords)
    passwords_col.set_item_name("password")

    table = forcetable.Table()
    # Set common record to be shared by all records
    common_record = forcetable.Record()
    common_record.add_item("submit", "login")
    table.set_common_record(common_record)
    # Add fields to table
    table.add_primary_field(usernames_col)
    table.add_field(passwords_col)

    producer = LoopSomeProducer(table)
    producer.set_excluded_primary_items(range(10))
    producer.add_excluded_primary_item(1)
    print(len(list(producer.get_items())))


    

    