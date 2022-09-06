<template>
    <div>

        <div  class="pt-3 col-12 d-flex justify-content-center justify-content-sm-between flex-wrap">
            <el-select
            class="select-primary mb-3 pagination-select"
            v-model="tablePagination.perPage"
            placeholder="Per page"
          >
            <el-option
              class="select-primary"
              v-for="item in tablePagination.perPageOptions"
              :key="item"
              :label="item"
              :value="item"
            >
            </el-option>
          </el-select>
          <base-input>
            <el-input
              type="search"
              class="mb-3 search-input"
              clearable
              prefix-icon="el-icon-search"
              placeholder="Search records"
              v-model="searchWord"
              aria-controls="datatables"
            >
            </el-input>
          </base-input>
        </div>
          <el-table
          header-cell-class-name="table-transparent"
          header-row-class-name="table-transparent"
          row-class-name="table-transparent"
          @sort="sortHandler"
            :data="spotTableData">
            <el-table-column :min-width="130" align="center" :label="$t('spots.findOnMap')">
              <div slot-scope="props">
                <base-button
                    @click.native="findSpot(props.$index, props.row)"
                    class="like btn-link"
                    type="info"
                    size="lg"
                    icon>
                  <i class="tim-icons icon-square-pin"></i>
                </base-button>
              </div>
            </el-table-column>
            <el-table-column
              v-for="column in spotTableColumns"
              sortable
              :key="column.label"
              :min-width="column.minWidth"
              :prop="column.prop"
              :label="column.label"
            >
            </el-table-column>
          </el-table>
        <div
        slot="footer"
        class="col-12 pt-3 d-flex justify-content-center justify-content-sm-between flex-wrap"
        >
        <div class="">
          <p class="card-category">
            {{$t('spots.entrytotal')}} {{ tablePagination.total }} {{$t('spots.entryshow')}} {{ tableFrom + 1 }}-{{ tableTo }}
          </p>
        </div>
        <base-pagination
          class="pagination-no-border"
          v-model="tablePagination.currentPage"
          :per-page="tablePagination.perPage"
          :total="tablePagination.total"
        >
        </base-pagination>
        </div>
    </div>
</template>
<script>


import { Table, TableColumn , Select, Option } from 'element-ui';
import { BasePagination } from 'src/components';
import _ from 'lodash'
import {getLikeSpotsList } from 'src/storage/userspots.js'

export default {

  components: {
    [Select.name]: Select,
    [Option.name]: Option,
    [Table.name]: Table,
    [TableColumn.name]: TableColumn,
    BasePagination,
  },
  data() {
    return {
      spotTableColumns: [
        {
          prop: 'idnumber',
          label: this.$t('table.idnumber'),
          minWidth: 100
        },
        {
          prop: 'spot_name',
          label: this.$t('table.name'),
          minWidth: 200
        },
        {
          prop: 'review_count',
          label: this.$t('table.review_count'),
          minWidth: 100
        },
        {
          prop: 'district',
          label: this.$t('table.district'),
          minWidth: 100
        },
        {
          prop: 'bike_number',
          label: this.$t('table.bike_number'),
          minWidth: 120
        },
        {
          prop: 'capacity',
          label: this.$t('table.capacity'),
          minWidth: 100
        },
        {
          prop: 'address',
          label: this.$t('table.address'),
          minWidth: 250
        },
        {
          prop: 'open_date',
          label: this.$t('table.open_date'),
          minWidth: 120
        }
        ],
      searchWord: '',
      tablePagination: {
        perPage: 5,
        currentPage: 1,
        perPageOptions: [5, 10, 25, 50],
        total: 0
      },
      spotTableData: [],
      userLikeSpots : [],
    }
  },
  computed: {
    tableTo() {
      let highBound = this.tableFrom + this.tablePagination.perPage;
      if (this.tablePagination.total < highBound) {
        highBound = this.tablePagination.total;
      }
      return highBound;
    },
    tableFrom() {
      return this.tablePagination.perPage * (this.tablePagination.currentPage - 1);
    },
  },
  methods : {

      getTableData() {
          let url = new URL(`http://localhost:8000/api/seoulbike/bikespot`)
      url.searchParams.append('page', this.tablePagination.currentPage)
      url.searchParams.append('page_size', this.tablePagination.perPage)
      url.searchParams.append('opened', 'True')
      if(!!this.searchWord){
        url.searchParams.append('search', this.searchWord)
      }
      this.$http.get(url.toString()).then((res)=>{
        this.spotTableData = res.data.results;
        console.log(this.spotTableData)
        this.tablePagination.total = res.data.count;
      }).catch((err)=>{
        this.$errorHandler(err);
      })
    },
    findSpot(index, row){
        this.$emit('findSpot', index, row)
    },
    sortHandler(value){
      console.log(value)
    }
    },
    watch : {
    'tablePagination.perPage' : function(value) {
      if(this.tablePagination.currentPage !== 1){
        this.tablePagination.currentPage = 1
      }else{
        this.getTableData()
      }
    },
    'tablePagination.currentPage' : function(value) {
      this.getTableData()
    },
    searchWord : _.debounce(function(){
      if(this.tablePagination.currentPage !== 1){
        this.tablePagination.currentPage = 1
      }else{
        this.getTableData()
      }
    }, 500,{
      'leading' : false,
      'trailing' : true
    }),
    userLikeSpots(value){
      this.getTableData()
    }
    },
    mounted(){
    this.getTableData()
    this.userLikeSpots = getLikeSpotsList()
    },




}



</script>