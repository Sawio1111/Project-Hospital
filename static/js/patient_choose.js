window.onload = () => {
    let form = document.querySelector('#form_id')
    let inputDate = document.querySelector('.datepickerinput')
    let prevDay = document.querySelector('#previous_day')
    let nextDay = document.querySelector('#next_day')
    let nextMonth = document.querySelector('#next_month')
    let prevMonth = document.querySelector('#previous_month')

    prevDay.addEventListener('click', (event) => {
        let date = new Date(inputDate.value)
        date = date.setDate(date.getDate() - 1);
        let next_day = new Date(date)
        inputDate.value = `${next_day.getFullYear()}-${(`0` + (next_day.getMonth() + 1)).slice(-2)}-${(`0` + next_day.getDate()).slice(-2)}`
        form.submit()
    })

    nextDay.addEventListener('click', (event) => {
        let date = new Date(inputDate.value)
        date = date.setDate(date.getDate() + 1);
        let next_day = new Date(date)
        inputDate.value = `${next_day.getFullYear()}-${(`0` + (next_day.getMonth() + 1)).slice(-2)}-${(`0` + next_day.getDate()).slice(-2)}`
        form.submit()
    })

    nextMonth.addEventListener('click', (event) => {
        let date = new Date(inputDate.value)
        date = date.setMonth(date.getMonth() + 1);
        let next_day = new Date(date)
        inputDate.value = `${next_day.getFullYear()}-${(`0` + (next_day.getMonth() + 1)).slice(-2)}-${(`0` + next_day.getDate()).slice(-2)}`
        form.submit()
    })

    prevMonth.addEventListener('click', (event) => {
        let date = new Date(inputDate.value)
        date = date.setMonth(date.getMonth() - 1);
        let next_day = new Date(date)
        inputDate.value = `${next_day.getFullYear()}-${(`0` + (next_day.getMonth() + 1)).slice(-2)}-${(`0` + next_day.getDate()).slice(-2)}`
        form.submit()
    })
}