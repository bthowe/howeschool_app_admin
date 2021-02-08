<!--                <li class="nav-item dropdown">-->
<!--                    <a class="nav-link dropdown-toggle" href="#" id="pagesDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">-->
<!--                        <i class="fas fa-fw fa-sun"></i>-->
<!--                        <span>Daily Input</span>-->
<!--                    </a>-->
<!--                    <div class="dropdown-menu bg-dark" aria-labelledby="pagesDropdown">-->
<!--                        <a class="dropdown-item bg-dark text-secondary" href="{{ url_for('enter_performance') }}">Math/Scripture</a>-->
<!--&lt;!&ndash;                        <a class="dropdown-item bg-dark text-secondary" href="{{ url_for('scripture_commentary') }}">Scripture</a>&ndash;&gt;-->
<!--                    </div>-->
<!--                </li>-->
<!--                <li class="nav-item dropdown">-->
<!--                    <a class="nav-link dropdown-toggle" href="#" id="pagesDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">-->
<!--                        <i class="fas fa-fw fa-calendar"></i>-->
<!--                        <span>Weekly Input</span>-->
<!--                    </a>-->
<!--                    <div class="dropdown-menu bg-dark" aria-labelledby="pagesDropdown">-->
<!--                        <a class="dropdown-item bg-dark text-secondary" href="{{ url_for('weekly_forms_create') }}">Forms</a>-->
<!--                        <a class="dropdown-item bg-dark text-secondary" href="{{ url_for('download_forms') }}">Download Forms</a>-->
<!--                    </div>-->
<!--                </li>-->
<!--                <li class="nav-item dropdown">-->
<!--                    <a class="nav-link dropdown-toggle" href="#" id="pagesDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">-->
<!--                        <i class="fas fa-fw fa-book"></i>-->
<!--                        <span>Math Book Input</span>-->
<!--                    </a>-->
<!--                    <div class="dropdown-menu bg-dark" aria-labelledby="pagesDropdown">-->
<!--                        <a class="dropdown-item bg-dark text-secondary" href="{{ url_for('enter_problem_number') }}">Number of exercises</a>-->
<!--                        <a class="dropdown-item bg-dark text-secondary" href="/enter_problem_origin">Origin of exercises</a>-->
<!--                    </div>-->
<!--                </li>-->
<!--                <li class="nav-item dropdown">-->
<!--                    <a class="nav-link dropdown-toggle" href="#" id="pagesDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">-->
<!--                        <i class="fas fa-fw fa-database"></i>-->
<!--                        <span>Database</span>-->
<!--                    </a>-->
<!--                    <div class="dropdown-menu bg-dark" aria-labelledby="pagesDropdown">-->
<!--                        <a class="dropdown-item bg-dark text-secondary" href="{{ url_for('database_viewer') }}">Table Viewer</a>-->
<!--                    </div>-->
<!--                </li>-->
<!--                <li class="nav-item dropdown">-->
<!--                    <a class="nav-link dropdown-toggle" href="#" id="pagesDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">-->
<!--                        <i class="fas fa-fw fa-users"></i>-->
<!--                        <span>Manage Accounts</span>-->
<!--                    </a>-->
<!--                    <div class="dropdown-menu bg-dark" aria-labelledby="pagesDropdown">-->
<!--                        <a class="dropdown-item bg-dark text-secondary" href="{{ url_for('register') }}">Register Child</a>-->
<!--{#                        <a class="dropdown-item bg-dark text-secondary" href="{{ url_for('database_viewer') }}">Database Viewer</a>#}-->
<!--                    </div>-->
<!--                </li>-->

<!--            {% endif %}-->

<!--                <li class="nav-item dropdown">-->
<!--                    <a class="nav-link dropdown-toggle" href="#" id="pagesDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">-->
<!--                        <i class="fas fa-fw fa-user-graduate"></i>-->
<!--                        <span>Study</span>-->
<!--                    </a>-->
<!--&lt;!&ndash;                    <div class="dropdown-menu bg-dark" aria-labelledby="pagesDropdown">&ndash;&gt;-->
<!--&lt;!&ndash;                        <a class="dropdown-item bg-dark text-secondary" href="{{ url_for('vocab') }}">Vocabulary</a>&ndash;&gt;-->
<!--&lt;!&ndash;                        <a class="dropdown-item bg-dark text-secondary" href="{{ url_for('math_todo') }}">Math to do</a>&ndash;&gt;-->
<!--&lt;!&ndash;                        <a class="dropdown-item bg-dark text-secondary" href="{{ url_for('sotw') }}">Scripture of the week</a>&ndash;&gt;-->
<!--&lt;!&ndash;                        <a class="dropdown-item bg-dark text-secondary" href="{{ url_for('qotw') }}">Questions of the week</a>&ndash;&gt;-->
<!--&lt;!&ndash;                    </div>&ndash;&gt;-->
<!--                </li>-->

<!--                {% if access == 2 %}-->
<!--                <li class="nav-item dropdown">-->
<!--                    <a class="nav-link dropdown-toggle" href="#" id="pagesDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">-->
<!--                        <i class="fas fa-fw fa-dollar-sign"></i>-->
<!--                        <span>Banking</span>-->
<!--                    </a>-->
<!--                    <div class="dropdown-menu bg-dark" aria-labelledby="pagesDropdown">-->
<!--                        <a class="dropdown-item bg-dark text-secondary" href="{{ url_for('banking_manage') }}">Manage Accounts</a>-->
<!--                        <a class="dropdown-item bg-dark text-secondary" href="{{ url_for('banking_history') }}">View History</a>-->
<!--                    </div>-->
<!--                </li>-->
<!--                {% elif access == 1 %}-->
<!--                <li class="nav-item dropdown">-->
<!--                    <a class="nav-link dropdown-toggle" href="#" id="pagesDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">-->
<!--                        <i class="fas fa-fw fa-folder"></i>-->
<!--                        <span>Banking</span>-->
<!--                    </a>-->
<!--                    <div class="dropdown-menu bg-dark" aria-labelledby="pagesDropdown">-->
<!--                        <a class="dropdown-item bg-dark text-secondary" href="{{ url_for('banking_history_personal') }}">View History</a>-->
<!--                    </div>-->
<!--                </li>-->
<!--                {% endif %}-->

<!--{#                <li class="nav-item">#}-->
<!--{#                    <a class="nav-link" href="other_stuff/tables.html">#}-->
<!--{#                        <i class="fas fa-fw fa-table"></i>#}-->
<!--{#                        <span>Tables</span></a>#}-->
<!--{#                </li>#}-->



<!--                        {% if page_name != "Main Menu" %}-->
<!--                            {% if page_name == "Vocabulary Practice" or page_name == "Vocabulary Quiz" %}-->
<!--                                <li class="breadcrumb-item active">-->
<!--                                    <a href="{{ url_for('vocab') }}">Vocabulary Menu</a>-->
<!--                                </li>-->
<!--                                <li class="breadcrumb-item active">{{ page_name }}: Lesson {{ lesson_num }}</li>-->
<!--                            {% else %}-->
<!--                                <li class="breadcrumb-item active">{{ page_name }}</li>-->
<!--                            {% endif %}-->

<!--                        {% endif %}-->
