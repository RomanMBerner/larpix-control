'''
Quickstart commands for test boards
'''

from __future__ import absolute_import
import larpix.larpix as larpix
from larpix.tasks import get_chip_ids


#List of LArPix test board configurations
board_info_list = [
    {'name':'unknown',
     'chip_list':[(chip_id,0) for chip_id in range(0,256)],},
    {'name':'pcb-5',
     'chip_list':[(246,0),(245,0),(252,0),(243,0)],},
    {'name':'pcb-4',
     'chip_list':[(207,0),(63,0),(250,0),(249,0)],},
    {'name':'pcb-1',
     'chip_list':[(246,0),(245,0),(252,0),(243,0)],},
]

#Create handy map by board name
board_info_map = dict([(elem['name'],elem) for elem in board_info_list])

def create_controller():
    '''Create a default controller'''
    return larpix.Controller()

def init_controller(controller, board='pcb-5'):
    '''Initialize controller'''
    if not board_info_map.has_key(board):
        board = 'unknown'
    board_info = board_info_map[board]
    for chip_info in board_info['chip_list']:
        controller.chips.append( larpix.Chip(chip_info[0],chip_info[1]) )
    controller.board_info = board_info
    return controller
        
def silence_chips(controller):
    '''Silence all chips in controller'''
    #for _ in controller.chips:
    for chip in controller.chips:
        chip.config.global_threshold = 255
        controller.write_configuration(chip,32)
    return

def disable_chips(controller):
    '''Silence all chips in controller'''
    #for _ in controller.chips:
    for chip in controller.chips:
        chip.config.disable_channels()
        controller.write_configuration(chip,range(52,56))
    return

def set_config_physics(controller, board=None):
    '''Set the chips for the default physics configuration'''
    #import time
    for chip in controller.chips:
        '''if not board is None:
            try:
                chip.config.load('physics-%s-c%d.json' % (board, chip.chip_id))
            except Exception as e:
                print('failed to load chip specific config - error: %s' % e)
                chip.config.load('physics.json')
        else:
            chip.config.load('physics.json')
        controller.write_configuration(chip)'''
        chip.config.internal_bypass = 1
        controller.write_configuration(chip,33)
        chip.config.periodic_reset = 1
        controller.write_configuration(chip,47)
        chip.config.global_threshold = 60
        controller.write_configuration(chip,32)
        chip.config.reset_cycles = 4096
        controller.write_configuration(chip,range(60,63))
        #time.sleep(2)
        print('configured chip %d' % chip.chip_id)
    return

def flush_stale_data(controller):
    '''Read and discard buffer contents'''
    controller.run(1,'flush_buffer')
    controller.reads = []
    return
    
def quickcontroller(board='pcb-1'):
    '''Quick jump through all controller creation and config steps'''
    larpix.enable_logger()
    cont = create_controller()
    init_controller(cont,board)
    silence_chips(cont)
    if cont.board_info['name'] == 'unknown':
        # Find and load chip info
        settings = {'controller':cont}
        cont.chips = get_chip_ids(**settings)
    set_config_physics(cont)
    flush_stale_data(cont)
    return cont

# Short-cut handle
qc = quickcontroller
